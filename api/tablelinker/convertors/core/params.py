from abc import ABC
import json
from logging import getLogger

from .validators import IntValidator, BooleanValidator, RequiredValidator

logger = getLogger(__name__)


class ParamSet(object):
    def __init__(self, *args):
        self._list = []
        self._dist = {}
        if len(args) == 1 and type(args[0]) is list:
            self.add(args[0])
        else:
            self.add(args)

    def __len__(self):
        return len(self._list)

    def __contains__(self, item):
        return [param for param in self._list if param.name == item]

    def __getitem__(self, item):
        return self._dist.get(item)

    def __add__(self, other):
        return self.add(other)

    def __iter__(self):
        return self.params().__iter__()

    def add(self, other):
        for o in other:
            self.append(o)

    def keys(self):
        return [param.key() for param in self._list]

    def params(self):
        return [param for param in self._list]

    def append(self, param):
        if param is None:
            return
        if param.name not in self._dist:
            self._list.append(param)
            self._dist[param.name] = param
        else:
            raise "duplicate key."  # FIXME

    def validate(self, param_values, errors, input=None, output=None):
        for param in self._list:
            key = param.key
            value = param_values[key] if key in param_values else None
            param.validate(
                value, errors, input=input, output=output,
            )
        return not errors.has_error()


class Param(ABC):
    def __init__(
        self,
        name,
        description=None,
        help_text=None,
        default_value=None,
        label=None,
        group=None,
        validators=None,
        required=False,
    ):
        self.name = name
        self.description = description
        self.help_text = help_text
        self.label = label if label is not None else self.name
        self.default_value = default_value
        self.group = group
        self.required = required

        self.validators = validators + self.default_validators() if validators is not None else self.default_validators()
        if required:
            self.validators = (RequiredValidator(),) + self.validators

    @property
    def key(self):
        """パラメータを特定するキー

        パラメータを特定する為のキー文字列です。
        """
        return self.name

    @property
    def type(self):
        """パラメータ毎の一意のキーです。
        """
        return self.Meta.type

    def default_validators(self):
        """
        """
        return ()

    def validate(self, value, errors, input=None, output=None):
        result = True
        for validator in self.validators:
            r = (
                validator(value, errors, input=input, output=output)
                if callable(validator)
                else validator.valid(value, errors, self, input=input, output=output)
            )
            if r is False:
                result = False
                if validator.stop_when_error():
                    break

        return result

    def parse_value(self, value):
        """Json化されて、文字列になっている値をパースします。

        例: return int(value)
        """
        return value

    def get_value(self, value, context):
        """値を取得するメソッドです。

        通常このメソッドを拡張する必要はありません。
        """
        if value is None:
            return self.default_value

        return self.parse_value(value)

    @property
    def arguments(self):
        return {}


class TextParam(Param):
    class Meta:
        type = "text"


class StringParam(Param):
    class Meta:
        type = "string"


class StringListParam(Param):
    class Meta:
        type = "string_list"


class IntParam(Param):
    class Meta:
        type = "integer"

    def default_validators(self):
        return (IntValidator(),)

    def parse_value(self, value):
        return int(value)


class EnumsParam(Param):
    class Meta:
        type = "enums"

    def __init__(self, *args, enums=None, labels=None, default_value: None, **kwargs):
        """
        :enums: Enumクラス 例:class Xxxx(Enum):...
        :enums_labels: Enumsのラベルハッシュ
        """
        super(EnumsParam, self).__init__(*args, **kwargs)
        self.enums = enums
        self.labels = labels
        self.default_value = default_value.value

    def parse_value(self, value):
        return self.enums(value)

    @property
    def arguments(self):
        enum_values = [{"value": str(enum.value), "label": self.labels[enum]} for enum in self.enums]
        return {
            "enums": json.dumps(enum_values),
        }


class BooleanParam(Param):
    class Meta:
        type = "boolean"

    def default_validators(self):
        return (BooleanValidator(),)

    def parse_value(self, value):
        if isinstance(value, str):
            if value.lower() == 'true':
                value = True
            else:
                value = False

        logger.warning("boolean: parse_value -> '{}'({})".format(
            str(value), type(value)))
        return value


class CollectionParam(Param):
    """
    他のコレクションを指定する為のパラメータ
    """

    class Meta:
        type = "collection"

    def get_value(self, value, context):
        return context.get_proxy(value)


class AttributeParam(Param):
    """
    列を指定するためのパラメータです。
    列のインデックスを返します。
    """

    class Meta:
        type = "attribute"

    def __init__(
        self,
        *args,
        collection_param_name=None,
        label_prefix=None,
        label_suffix=None,
        empty=False,
        empty_value=None,
        empty_label=None,
        **kwargs
    ):
        super(AttributeParam, self).__init__(*args, **kwargs)
        self.collection_param_name = collection_param_name
        self.label_prefix = label_prefix
        self.label_suffix = label_suffix
        self.empty = empty
        self.empty_value = empty_value
        self.empty_label = empty_label

    @property
    def arguments(self):
        return {
            "collection_param_name": self.collection_param_name,
            "label_prefix": self.label_prefix,
            "label_suffix": self.label_suffix,
            "empty": self.empty,
            "empty_value": self.empty_value,
            "empty_label": self.empty_label,
        }

    # def default_validators(self):
    #     return (IntValidator(),)


class AttributeListParam(Param):
    """
    複数の列を指定するためのパラメータ
    """

    class Meta:
        type = "attribute-list"

    def __init__(self, *args, collection_param_name=None, **kwargs):
        super(AttributeListParam, self).__init__(*args, **kwargs)
        self.collection_param_name = collection_param_name

    def parse_value(self, value):
        return [int(val) for val in value]

    @property
    def arguments(self):
        return {"collection_param_name": self.collection_param_name}

    def default_validators(self):
        return ()


class InputAttributeParam(AttributeParam):
    """
    入力列を指定するためのパラメータです。
    列のインデックスを返します。
    """

    class Meta:
        type = "input-attribute"


class InputAttributeListParam(AttributeParam):
    """
    入力列を指定するためのパラメータです。
    列のインデックスを返します。
    """

    class Meta:
        type = "input-attribute-list"


class OutputAttributeParam(StringParam):
    """
    新規列の為のパラメータです。
    """

    class Meta:
        type = "output-attribute"

    def __init__(self, *args, prefix=False, **kwargs):
        super(OutputAttributeParam, self).__init__(*args, **kwargs)
        self.prefix = prefix

    @property
    def arguments(self):
        return {"prefix": self.prefix}


class OutputAttributeListParam(AttributeListParam):
    """
    複数の列を指定するためのパラメータ
    """

    class Meta:
        type = "output-attribute-list"
