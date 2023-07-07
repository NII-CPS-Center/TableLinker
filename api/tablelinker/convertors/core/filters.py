from abc import ABC
from . import params


class FilterMeta(object):
    def __init__(self, meta):
        self.key = meta.key
        self.name = meta.name
        self.description = meta.description
        self.message = meta.message if hasattr(meta, "message") else meta.description or ""
        self.help_text = meta.help_text
        self.params = meta.params

    @property
    def input_params(self):
        return [param for param in self.params if param.Meta.type == "input-attribute"]

    @property
    def output_params(self):
        return [param for param in self.params if param.Meta.type == "output-attribute"]


class Filter(ABC):
    """
    変換処理
    """

    @classmethod
    def meta(cls):
        return FilterMeta(cls.Meta)

    @classmethod
    def key(cls):
        return cls.meta().key

    @property
    def params(self):
        return self.__class__.meta().params

    def process(self, context):
        self.initial_context(context)
        self.initial(context)
        context.reset()

        self.process_header(context.next(), context)
        for record in context.read():
            if not self.check_process_record(record, context):
                continue
            self.process_record(record, context)

    def initial_context(self, context):
        headers = context.next()
        context.set_data("headers", headers)
        context.set_data("num_of_columns", len(headers))

    def initial(self, context):
        pass

    def process_header(self, headers, context):
        context.output(headers)

    def check_process_record(self, record, context):
        """
        入力するレコードへのチェックを行います。
        :return: boolean
        """
        if context.get_data("num_of_columns") != len(record):
            return False
        else:
            return True

    def process_record(self, record, context):
        context.output(record)

    @classmethod
    def can_apply(cls, attrs):
        """
        対象の属性がこのフィルタに適用可能かどうかを返します。
        attrs: 属性のリスト({name, attr_type, data_type})
        """
        return True

    @classmethod
    def get_message(cls, params):
        """
        変換時に追加するメッセージを生成します。
        params: パラメータのリストです。
        """
        return cls.meta().message.format(**params)


class InputOutputFilter(Filter):
    @classmethod
    def meta(cls):
        _meta = FilterMeta(cls.Meta)
        _meta.params = params.ParamSet(
            [
                params.InputAttributeParam("input_attr_idx", label="入力列", description="処理をする対象の列", required=True),
                params.OutputAttributeParam(
                    "output_attr_name",
                    label="出力列名",
                    description="変換結果を出力する列名です。",
                    help_text="空もしくは既存の名前が指定された場合、置換となります。",
                    required=False,
                ),
                params.AttributeParam(
                    "output_attr_new_index",
                    label="出力列の位置",
                    description="新しい列の挿入位置です。",
                    label_suffix="の後",
                    empty=True,
                    empty_label="先頭",
                    required=False,
                ),
            ]
            + _meta.params.params()
        )
        return _meta

    @classmethod
    def can_apply(cls, attrs):
        """
        対象の属性がこのフィルタに適用可能かどうかを返します。
        attrs: 属性のリスト({name, attr_type, data_type})
        """
        if len(attrs) != 1:
            return False
        return True

    def initial(self, context):
        self.output_attr_index = None
        self.new_attr = None

    def process_header(self, header, context):
        output_attr_name = context.get_param("output_attr_name")
        input_attr_idx = context.get_param("input_attr_idx")

        if output_attr_name is None:
            self.output_attr_index = input_attr_idx  # Noneの場合は、置換
            self.new_attr = False
        else:
            # 既存列か調べる
            try:
                self.output_attr_index = header.index(output_attr_name)
                self.new_attr = False
            except ValueError:
                # 新規列の追加
                self.output_attr_index = len(header)
                self.new_attr = True
                header.append(output_attr_name)

        # 移動
        output_attr_new_index = context.get_param("output_attr_new_index")
        if output_attr_new_index is None:  # 先頭
            header.insert(0, header.pop(self.output_attr_index))
        else:  # 指定位置
            header.insert(output_attr_new_index + 1, header.pop(self.output_attr_index))

        context.output(header)

    def process_record(self, record, context):
        input_attr_idx = context.get_param("input_attr_idx")

        value = self.process_filter(input_attr_idx, record, context)

        if self.output_attr_index < len(record):
            record[self.output_attr_index] = value
        else:
            record.insert(self.output_attr_index, value)

        # 移動
        output_attr_new_index = context.get_param("output_attr_new_index")
        if output_attr_new_index is None:  # 先頭
            record.insert(0, record.pop(self.output_attr_index))
        else:  # 指定位置
            record.insert(output_attr_new_index + 1, record.pop(self.output_attr_index))

        context.output(record)

    def process_filter(self, input_attr_idx, record, context):
        return record[input_attr_idx]


class NoopFilter(Filter):
    """
    何もしない
    """

    class Meta:
        key = "noop"
        name = "何もしません"
        description = None
        help_text = None
        params = params.ParamSet()


class AttrCopyFilter(InputOutputFilter):
    """
    列コピー
    """

    class Meta:
        key = "acopy"
        name = "列のコピー"
        description = "列をコピーします"
        help_text = None
        params = params.ParamSet()


FILTERS = [AttrCopyFilter]
FILTER_DICT = {}
for f in FILTERS:
    FILTER_DICT[f.key()] = f


def registry_filter(filter, selectable=True):
    """
    フィルタを登録します。
    filter: フィルタクラス
    selectable: ユーザが選択可能なフィルターかどうか
    """
    if selectable:
        FILTERS.append(filter)
    FILTER_DICT[filter.key()] = filter


def filter_find_by(name):
    return FILTER_DICT.get(name)


def filter_all():
    return [f for f in FILTERS]


def filter_meta_list(attrs=[]):
    """
    適用可能なフィルタのメタ情報を取得します。
    """
    _attrs = attrs if attrs is not None else []
    return [filter.meta() for filter in filter_all() if filter.can_apply(_attrs)]


def filter_keys():
    return [f.Meta.key for f in FILTERS]


def encode_filter(filter):
    return [filter.key()]


def decode_filter(filter):
    return filter_find_by(filter[0])()
