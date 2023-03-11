import MySQLdb
import aprslib
import yaml
import logging
import time

with open("configuration.yaml", 'r') as stream:
    configuration = yaml.safe_load(stream)

formatter = logging.Formatter(fmt='<%(asctime)s> [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger()
logger.setLevel(configuration['logging']['level'])

sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

fh = logging.FileHandler(filename='logs/' + str(configuration['logging']['level']).lower() + '.log', mode='a')
fh.setFormatter(formatter)
logger.addHandler(fh)

if configuration['mysql']['unix_socket']:
    db = MySQLdb.connect(
        unix_socket=configuration['mysql']['unix_socket'],
        user=configuration['mysql']['username'],
        password=configuration['mysql']['password'],
        database=configuration['mysql']['database'],
    )
else:
    db = MySQLdb.connect(
        host=configuration['mysql']['hostname'],
        user=configuration['mysql']['username'],
        password=configuration['mysql']['password'],
        database=configuration['mysql']['database'],
    )

last_flush = 0


def flush_history(keep=500):
    global last_flush

    if (time.time() - last_flush) > 60:
        crs = db.cursor()
        # Keep only last *keep* rows for each call sign
        try:
            crs.execute("""
            DELETE `h3`
            FROM `history` `h3`
            WHERE `h3`.`date` < (
            SELECT `t`.`date`
            FROM (SELECT `h1`.`call_sign`,
                         (SELECT `h2`.`date`
                          FROM `history` `h2`
                          WHERE `h2`.`call_sign` = `h1`.`call_sign`
                          ORDER BY `h2`.`date` DESC
                          LIMIT %s, 1) AS `date`
                  FROM `history` `h1`
                  GROUP BY `h1`.`call_sign`) `t`
            WHERE `h3`.`call_sign` = `t`.`call_sign` AND `t`.`date` IS NOT NULL
            );
            """, (keep - 1,))
        except Exception as exception:
            logging.error("MySQL Error: " + str(exception))
        finally:
            crs.close()

        logging.info("History flushed")
        last_flush = time.time()


def callback(packet):
    if configuration['history']['keep'] != 'all':
        flush_history(keep=configuration['history']['keep'])

    try:
        parsed = aprslib.parse(packet)
    except (aprslib.ParseError, aprslib.UnknownFormat) as exception:
        logging.warning(packet + " ignored: can't be parsed (" + exception + ")")
        return

    q = parsed.get('path')[-2]
    if q not in ['qAR', 'qAO', 'qAo']:
        logging.info(parsed.get('from') + " ignored: q construct prohibited (" + q + "," + parsed.get('via') + "; " + parsed.get("comment") + ")")
        return

    if parsed.get('latitude') is None or parsed.get('longitude') is None:
        logging.info(parsed.get('from') + " ignored: empty coordinates")
        return

    if 0.1 > parsed.get('latitude') > -0.1 and 0.1 > parsed.get('longitude') > -0.1:
        logging.warning(parsed.get('from') + " ignored: GPS positioning error (" + str(parsed.get('latitude')) + "," + str(parsed.get('longitude')) + "; via " + parsed.get('via') + ")")
        return

    insert_query = """INSERT INTO
        `history`
    SET
        `call_sign` = %s,
        `date` = UTC_TIMESTAMP(),
        `comment` = %s,
        `latitude` = %s,
        `longitude` = %s,
        `raw` = %s
    ON DUPLICATE KEY
        UPDATE
            `call_sign` = %s,
            `date` = UTC_TIMESTAMP(),
            `comment` = %s,
            `latitude` = %s,
            `longitude` = %s,
            `raw` = %s
    ;"""
    insert_params = (
        parsed.get('from'),
        parsed.get('comment'),
        parsed.get('latitude'),
        parsed.get('longitude'),
        parsed.get('raw'),

        parsed.get('from'),
        parsed.get('comment'),
        parsed.get('latitude'),
        parsed.get('longitude'),
        parsed.get('raw')
    )

    crs = db.cursor()
    try:
        crs.execute(insert_query, insert_params)
        db.commit()
    except Exception as exception:
        logging.error("MySQL Error during inserting new row: " + str(exception))
        db.rollback()
    finally:
        crs.close()

    logging.info(parsed.get('from') + " saved")


try:
    logging.warning("Program starting")
    AIS = aprslib.IS(configuration['aprs']['callsign'], passwd="-1", host=configuration['aprs']['host'], port=configuration['aprs']['port'])
    AIS.set_filter(configuration['aprs']['filter'])
    AIS.connect()
    AIS.consumer(callback, raw=True)
except Exception as e:
    trace = []
    tb = e.__traceback__
    while tb is not None:
        trace.append(tb.tb_frame.f_code.co_filename + ": " + str(tb.tb_lineno))
        tb = tb.tb_next

    logging.error("APRS-IS Client Error: " + type(e).__name__ + ": " + str(e) + " >>> " + ", ".join(trace))
except KeyboardInterrupt:
    logging.info("Received closing command from user")
finally:
    logging.warning("Program stopping")
    db.close()
