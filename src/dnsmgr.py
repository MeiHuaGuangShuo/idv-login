# coding=UTF-8
"""
 Copyright (c) 2024 Alexander-Porter & fwilliamhe

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.
 """

import dns.message
import dns.query
import dns.rdatatype
from logger import logger


class InvalidHostName(Exception):
    pass


class DNSResolver(object):

    def __init__(self):
        self.logger = logger

    def gethostbyname(self, hostname):
        answers=[]
        q = dns.message.make_query(hostname, dns.rdatatype.A)
        r = dns.query.udp(q,"114.114.114.114")
        for answer in r.answer:
            answers.append(str(list(answer.items.keys())[0]))
        if answers:
            return answers[-1]
        else:
            return None