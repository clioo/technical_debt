import json
import datetime
from typing import Dict
import uuid

from core.config import APP_VERSION, get_settings, ENV, MICROSERVICE
from db.session import create_db_connection

settings = get_settings()


INSERT_QUERY = """
    INSERT INTO {log_table}
    (execution_time, log_uuid, user_agent, ip, [datetime], input, output, env,
     microservice, app_version)
    VALUES({execution_time}, '{log_uuid}', '{user_agent}', '{ip}',
           '{datetime_now}', '{input}', '{output}', '{env}', '{microservice}',
           '{app_version}');
"""


async def save_logs(
    database: str,
    execution_time: float,
    prefix: str = None,
    user_agent: str = None,
    ip: str = None,
    output: Dict = None,
    input: Dict = None,
):
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_uuid = str(uuid.uuid4())
    log_uuid = f"{prefix}-{log_uuid}" if prefix else log_uuid
    user_agent = user_agent[:100]
    query = INSERT_QUERY.format(
        log_table=settings.log_table,
        execution_time=execution_time,
        log_uuid=log_uuid,
        user_agent=user_agent,
        ip=ip,
        datetime_now=datetime_now,
        input=json.dumps(input),
        output=json.dumps(output),
        env=ENV,
        microservice=MICROSERVICE,
        app_version=APP_VERSION,
    )
    session, _ = create_db_connection(database)
    session.execute(query)
    session.commit()
