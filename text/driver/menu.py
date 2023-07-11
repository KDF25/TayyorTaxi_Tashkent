from string import Template
from aiogram.utils.markdown import hlink
from text.language.main import Text_main

Txt = Text_main()


class FormMenuDriver:
    def __init__(self, language: str):
        self.__Text_lang = Txt.language[language]

    async def main(self):
        text = Template('$main\n\n'
                        '👉$text1')
        text = text.substitute(main=self.__Text_lang.greeting.main,
                               text1=hlink(url=self.__Text_lang.url.client.how_to_use,
                                           title=self.__Text_lang.information.how_to_use))
        return text

    async def how_to_use(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Text_lang.url.client.how_to_use,
                                           title=self.__Text_lang.information.how_to_use))
        return text

    async def about_us(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Text_lang.url.client.about_us,
                                           title=self.__Text_lang.information.about_us))
        return text


