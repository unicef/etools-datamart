from unittest import mock

from etools_datamart.libs.constance import ObfuscatedInput, WriteOnlyInput, WriteOnlyTextarea


def check_html(widget, name, value, html='', attrs=None, strict=False, **kwargs):
    output = widget.render(name, value, attrs=attrs, renderer=None, **kwargs)
    assert output == html


class TestWriteOnlyTextarea:
    widget = WriteOnlyTextarea()

    def test_render(self):
        assert self.widget.render('name', '') == '''<textarea name="name" cols="40" rows="10">
***</textarea>'''

    def test_value_from_datadict(self):
        with mock.patch("etools_datamart.libs.constance.config", mock.Mock(NAME="abc")):
            assert self.widget.value_from_datadict({"NAME": "***"}, {}, 'NAME') == "abc"
            assert self.widget.value_from_datadict({"NAME": "123"}, {}, 'NAME') == "123"


class TestWriteOnlyInput:
    widget = WriteOnlyInput()

    def test_render(self):
        assert self.widget.render('name', '') == '<input type="text" name="name" value="***">'

    def test_value_from_datadict(self):
        with mock.patch("etools_datamart.libs.constance.config", mock.Mock(NAME="abc")):
            assert self.widget.value_from_datadict({"NAME": "***"}, {}, 'NAME') == "abc"
            assert self.widget.value_from_datadict({"NAME": "123"}, {}, 'NAME') == "123"


class TestObfuscatedInput:
    widget = ObfuscatedInput()

    def test_render(self):
        assert self.widget.render('name', '') == '<input type="hidden" name="name" value="">Not Set'

    def test_value_from_datadict(self):
        assert self.widget.value_from_datadict({"NAME": "***"}, {}, 'NAME') == "***"
