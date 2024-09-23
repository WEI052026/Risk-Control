from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.text import LabelBase

# 註冊字型
LabelBase.register(name="NotoSans", fn_regular="C:/Users/黃浩瑋/OneDrive/桌面/NotoSansTC-VariableFont_wght.ttf")

class CustomSlider(Slider):
    def __init__(self, **kwargs):
        super(CustomSlider, self).__init__(**kwargs)
        self.bind(value=self.update_thumb_pos)

    def update_thumb_pos(self, *args):
        pass  # 這裡保留，但不執行任何操作

class InvestmentCalculator(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # 設定字體大小
        font_size = '24sp'  # 調整字體大小

        # 輸入框：開倉價、止損價、想要承擔的虧損金額
        self.entry_price_input = TextInput(hint_text="輸入開倉價格", multiline=False, font_name="NotoSans", font_size=font_size)
        self.stop_loss_input = TextInput(hint_text="輸入止損價格", multiline=False, font_name="NotoSans", font_size=font_size)

        # 使用自定義的滑桿
        self.leverage_slider = CustomSlider(min=1, max=100, value=10)  # 槓桿滑桿
        self.leverage_label = Label(text=f"槓桿: {int(self.leverage_slider.value)}倍", font_name="NotoSans", font_size=font_size)
        self.loss_input = TextInput(hint_text="最大虧損金額", multiline=False, font_name="NotoSans", font_size=font_size)

        # 槓桿滑桿變動時更新顯示
        self.leverage_slider.bind(value=self.update_leverage_label)

        # 按鈕：計算倉位大小
        calc_button = Button(text="計算倉位大小", on_press=self.calculate_position_size, font_name="NotoSans", font_size=font_size)

        # 顯示計算結果的標籤
        self.result_label = Label(text="倉位大小: ", font_name="NotoSans", font_size=font_size)
        self.margin_label = Label(text="保證金: ", font_name="NotoSans", font_size=font_size)  # 保證金標籤

        # 將各個元件添加到佈局中
        layout.add_widget(self.entry_price_input)
        layout.add_widget(self.stop_loss_input)
        layout.add_widget(self.leverage_label)
        layout.add_widget(self.leverage_slider)
        layout.add_widget(self.loss_input)
        layout.add_widget(calc_button)

        # 使用水平佈局來顯示倉位大小和保證金
        result_layout = BoxLayout(size_hint_y=None, height=50)
        result_layout.add_widget(self.result_label)
        result_layout.add_widget(self.margin_label)  # 添加保證金標籤到結果佈局

        layout.add_widget(result_layout)

        return layout

    def update_leverage_label(self, instance, value):
        self.leverage_label.text = f"槓桿: {int(value)}倍"  # 確保槓桿值是整數

    def calculate_position_size(self, instance):
        try:
            entry_price = float(self.entry_price_input.text)
            stop_loss = float(self.stop_loss_input.text)
            desired_loss = float(self.loss_input.text)

            # 計算每單位風險
            risk_per_unit = abs(entry_price - stop_loss)

            # 計算倉位大小
            position_size = (desired_loss / risk_per_unit) * entry_price
            self.result_label.text = f"倉位大小: ${position_size:.2f}"

            # 計算保證金，無條件捨去小數點
            margin = position_size // int(self.leverage_slider.value)
            self.margin_label.text = f"保證金: ${margin:.2f}"

        except ValueError:
            self.result_label.text = "請輸入有效數字"
            self.margin_label.text = "保證金: "

if __name__ == "__main__":
    InvestmentCalculator().run()
