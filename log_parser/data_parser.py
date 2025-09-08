from loguru import logger
import statistics
import re

from log_parser.application.utils import get_re_model


class LogParser:
    def __init__(self, log_file: str, re_model_path: str):
        self.log_file = log_file
        self.re_model = get_re_model(re_model_path)

    async def parse_line(self, log_line: str) -> tuple:
        log_pattern = re.compile(self.re_model)
        match = log_pattern.match(log_line)
        if match:
            data = match.groupdict()
            return (
                data["ip"],
                data["datetime"],
                data["method"],
                data["path"],
                int(data["status"]),
                int(data["size"]),
                data["referer"],
                data["user_agent"],
                int(data["response_time"]),
            )
        else:
            logger.error(f"Failed to parse log line, wrong format")

    async def parse_logs(self) -> list:
        results = []
        with open(self.log_file, "r") as file:
            for line in file.readlines():
                try:
                    data = await self.parse_line(line)
                    results.append(data)
                except Exception as e:
                    logger.error(
                        f"Failed to parse log line: {e.__class__.__name__}, {e}"
                    )
        return results

    async def get_statistics(self, data: list) -> dict:
        statuses = {i: [i[4] for i in data].count(i) for i in set([j[4] for j in data])}
        endpoints = {
            i: [i[3] for i in data].count(i) for i in set([j[3] for j in data])
        }
        methods = {i: [i[2] for i in data].count(i) for i in set([j[2] for j in data])}
        ips = {i: [i[0] for i in data].count(i) for i in set([j[0] for j in data])}
        response_time_data = [i[-1] for i in data]
        statistics_data = {
            "response_statuses": statuses,
            "average_time": round(sum(response_time_data) / len(response_time_data), 3),
            "median_time": statistics.median(response_time_data),
            "endpoints": endpoints,
            "ips": ips,
            "methods": methods,
        }
        return statistics_data
