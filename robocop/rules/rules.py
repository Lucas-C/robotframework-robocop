"""
Every issue is reported as ``robocop.rules.Rule`` object. It can be later printed or used by
post-run reports.

Format output message
---------------------

Output rule message can be defined with ``-f`` / ``--format`` argument. Default value::

    {source}:{line}:{col} [{severity}] {rule_id} {desc}

Available formats:
  * source: path to file where is the issue
  * line: line number
  * col: column number
  * severity: severity of the message. Value of enum ``robocop.rules.RuleSeverity``
  * rule_id: rule id (ie. 0501)
  * rule_name: rule name (ie. line-too-long)
  * desc: description of rule
"""
from enum import Enum
from copy import deepcopy
from functools import total_ordering
import robocop.exceptions


@total_ordering
class RuleSeverity(Enum):
    """
    Rule severity.
    It can be configured with ``-c/--configure id_or_msg_name:severity:value``
    Where value can be first letter of severity value or whole name, case insensitive.
    For example ::

        -c line-too-long:severity:e

    Will change line-too-long message severity to error.

    You can filter out all rules below given severity value by using following option::

        -t/--threshold <severity value>

    Example::

        --threshold E

    Will only report rules with severity E and above.
    """
    INFO = "I"
    WARNING = "W"
    ERROR = "E"
    FATAL = "F"

    def __lt__(self, other):
        look_up = [sev.value for sev in RuleSeverity]
        if self.__class__ is other.__class__:
            return look_up.index(self.value) < look_up.index(other.value)
        if isinstance(other, str):
            return look_up.index(self.value) < look_up.index(other)
        return NotImplemented


class Rule:
    def __init__(self, rule_id, body):
        self.rule_id = rule_id
        self.name = ''
        self.desc = ''
        self.source = None
        self.enabled = True
        self.severity = RuleSeverity.INFO
        self.configurable = []
        self.parse_body(body)

    def __str__(self):
        return f'Rule - {self.rule_id} [{self.severity.value}]: {self.name}: {self.desc} ' \
               f'({"enabled" if self.enabled else "disabled"})'

    def change_severity(self, value):
        severity = {
            'error': 'E',
            'e': 'E',
            'warning': 'W',
            'w': 'W',
            'info': 'I',
            'i': 'I',
            'fatal': 'F',
            'f': 'F'
        }.get(str(value).lower(), None)
        if severity is None:
            raise robocop.exceptions.InvalidRuleSeverityError(self.name, value)
        self.severity = RuleSeverity(severity)

    def get_fullname(self):
        return f"{self.severity.value}{self.rule_id} ({self.name})"

    def get_configurable(self, param):
        for configurable in self.configurable:
            if configurable[0] == param:
                return configurable
        return None

    def parse_body(self, body):
        if isinstance(body, tuple) and len(body) >= 3:
            self.name, self.desc, self.severity, *self.configurable = body
        else:
            raise robocop.exceptions.InvalidRuleBodyError(self.rule_id, body)
        for configurable in self.configurable:
            if not isinstance(configurable, tuple) or len(configurable) != 3:
                raise robocop.exceptions.InvalidRuleConfigurableError(self.rule_id, body)

    def prepare_message(self, *args, source, node, lineno, col):
        message = deepcopy(self)
        try:
            message.desc %= args
        except TypeError as err:
            raise robocop.exceptions.InvalidRuleUsageError(self.rule_id, err)
        message.source = source
        if lineno is None and node is not None:
            lineno = node.lineno
        message.line = lineno
        if col is None:
            col = 0
        message.col = col
        return message
