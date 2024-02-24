import wx
from client_logic import *
from pubsub import pub
from client_protocol import ClientProtocol
import wx.lib.scrolledpanel
from wx.adv import Animation, AnimationCtrl
import wx.lib.intctrl
import wx, wx.lib.agw.rulerctrl as rc
import wx.lib.scrolledpanel


class LogIn(wx.Panel):
    """login panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        box = wx.BoxSizer(wx.VERTICAL)  # vertical sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)  # sizer for buttons
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)  # sizer for username
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)  # sizer for password
        box.AddSpacer(30)

        self.SetBackgroundColour('#D14081')
        # title
        btn_font = wx.Font(15,  wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)    # font
        txt_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font

        # logo
        png = wx.Image('logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # logo image
        self.bitmap = wx.StaticBitmap(self, -1, png, (png.GetWidth(), png.GetHeight()))
        box.Add(self.bitmap, 0, wx.ALIGN_CENTER)
        box.AddSpacer(80)

        # enter password and username
        self.username_txt = wx.StaticText(self, -1, "username: ")  # username
        self.username_txt.SetFont(btn_font)
        self.password_txt = wx.StaticText(self, -1, "password: ")  # password
        self.password_txt.SetFont(btn_font)

        self.username = wx.TextCtrl(self, size=(200, 30))
        self.username.SetFont(txt_font)
        self.password = wx.TextCtrl(self, size=(200, 30), style=wx.TE_PASSWORD)
        self.password.SetFont(txt_font)

        # adding username
        username_sizer.Add(self.username_txt, 0)
        username_sizer.AddSpacer(10)
        username_sizer.Add(self.username, 0)
        box.Add(username_sizer, 0, wx.ALIGN_CENTER)

        box.AddSpacer(150)

        # adding password
        password_sizer.Add(self.password_txt, 0)
        password_sizer.AddSpacer(10)
        password_sizer.Add(self.password, 0)
        box.Add(password_sizer, 0, wx.ALIGN_CENTER)

        box.AddSpacer(100)

        # creating buttons
        self.log_in = wx.Button(self, -1, "log in")     # log in btn
        self.sign_in = wx.Button(self, -1, "sign up")    # sign in btn
        self.log_in.SetSize((100, 50))
        self.sign_in.SetSize((100, 50))

        # buttons settings
        self.log_in.SetFont(btn_font)
        self.sign_in.SetFont(btn_font)
        self.log_in.SetBackgroundColour((255, 255, 255, 255))
        self.sign_in.SetBackgroundColour((255, 255, 255, 255))

        # adding btns
        btn_sizer.Add(self.log_in, 0)
        btn_sizer.AddSpacer(200)
        btn_sizer.Add(self.sign_in, 0)
        box.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        # alignments
        self.SetSizer(box)


class SignIn(wx.Panel):
    """sign in panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        box = wx.BoxSizer(wx.VERTICAL)  # vertical sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)  # sizer for buttons
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)  # sizer for username
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)  # sizer for password

        box.AddSpacer(50)

        self.SetBackgroundColour('#D14081')
        # title
        btn_font = wx.Font(15,  wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        txt_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font

        # logo
        png = wx.Image('logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # logo image
        self.bitmap = wx.StaticBitmap(self, -1, png, (png.GetWidth(), png.GetHeight()))
        box.Add(self.bitmap, 0, wx.ALIGN_CENTER)
        box.AddSpacer(80)

        # enter password and username
        self.username_txt = wx.StaticText(self, -1, "username: ")  # username
        self.username_txt.SetFont(btn_font)
        self.password_txt = wx.StaticText(self, -1, "password: ")  # password
        self.password_txt.SetFont(btn_font)

        self.username = wx.TextCtrl(self, size=(200, 30))
        self.username.SetFont(txt_font)
        self.password = wx.TextCtrl(self, size=(200, 30), style=wx.TE_PASSWORD)
        self.password.SetFont(txt_font)

        # adding username
        username_sizer.Add(self.username_txt, 0)
        username_sizer.AddSpacer(10)
        username_sizer.Add(self.username, 0)
        box.Add(username_sizer, 0, wx.ALIGN_CENTER)

        box.AddSpacer(150)

        # adding password
        password_sizer.Add(self.password_txt, 0)
        password_sizer.AddSpacer(10)
        password_sizer.Add(self.password, 0)
        box.Add(password_sizer, 0, wx.ALIGN_CENTER)

        box.AddSpacer(100)

        # creating buttons
        self.back = wx.Button(self, -1, "back")  # log in btn
        self.sign_in = wx.Button(self, -1, "sign up")  # sign in btn
        self.back.SetSize((100, 50))
        self.sign_in.SetSize((100, 50))

        # buttons settings
        self.back.SetFont(btn_font)
        self.back.SetForegroundColour(wx.Colour(255, 255, 255))
        self.sign_in.SetFont(btn_font)
        self.back.SetBackgroundColour((0, 0, 0, 0))
        self.sign_in.SetBackgroundColour((255, 255, 255, 255))

        # adding btns
        btn_sizer.Add(self.back, 0)
        btn_sizer.AddSpacer(200)
        btn_sizer.Add(self.sign_in, 0)
        box.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        # alignments
        self.SetSizer(box)


class Home(wx.Panel):
    """sign in panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.edit_files = []    # list of edit files
        box = wx.BoxSizer(wx.VERTICAL)  # vertical sizer

        box.AddSpacer(50)

        # logo
        png = wx.Image('logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # logo image
        self.bitmap = wx.StaticBitmap(self, -1, png, (png.GetWidth(), png.GetHeight()))
        box.Add(self.bitmap, 0, wx.ALIGN_CENTER)

        self.SetBackgroundColour('#D14081')
        # title
        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        txt_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font

        # choose file text
        cblbl = wx.StaticText(self, label="choose file:", style=wx.ALIGN_CENTRE)
        cblbl.SetFont(txt_font)
        box.Add(cblbl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)

        # combo to select files
        self.choice_box = wx.Choice(self, choices=self.edit_files, size=(610, 50))
        font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font
        self.choice_box.SetFont(font)
        box.AddSpacer(10)
        box.Add(self.choice_box, 0, wx.ALIGN_CENTER_HORIZONTAL)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # buttons
        self.edit_file = wx.Button(self, -1, "edit file")  # edit file btn
        self.add_file = wx.Button(self, -1, "add file")  # add file in btn
        self.edit_file.SetSize((100, 50))
        self.add_file.SetSize((100, 50))

        # buttons settings
        self.edit_file.SetFont(btn_font)
        self.add_file.SetFont(btn_font)
        self.edit_file.SetBackgroundColour((255, 255, 255, 255))
        self.add_file.SetBackgroundColour((255, 255, 255, 255))

        # adding btns
        btn_sizer.Add(self.edit_file, 0)
        btn_sizer.AddSpacer(200)
        btn_sizer.Add(self.add_file, 0)
        box.AddSpacer(300)

        box.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # alignments
        self.SetSizer(box)


class AddFile(wx.Panel):
    """add file panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.usernames = []    # list of users
        box = wx.BoxSizer(wx.VERTICAL)  # vertical sizer

        box.AddSpacer(50)

        # logo
        png = wx.Image('logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # logo image
        self.bitmap = wx.StaticBitmap(self, -1, png, (png.GetWidth(), png.GetHeight()))
        box.Add(self.bitmap, 0, wx.ALIGN_CENTER)

        self.SetBackgroundColour('#D14081')
        # title
        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        txt_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font

        # choose file text
        cblbl = wx.StaticText(self, label="select users to edit with", style=wx.ALIGN_CENTRE)
        cblbl.SetFont(txt_font)
        box.Add(cblbl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)

        # check list box to select users
        self.choice_box = wx.CheckListBox(self, -1, choices=self.usernames, size=(610, 100))
        font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font
        self.choice_box.SetFont(font)
        box.AddSpacer(10)
        box.Add(self.choice_box, 0, wx.ALIGN_CENTER_HORIZONTAL)

        box.AddSpacer(100)

        # text ctrl to fill file name
        file_txt = wx.StaticText(self, label="enter file name", style=wx.ALIGN_CENTRE)
        file_txt.SetFont(txt_font)
        self.file_name = wx.TextCtrl(self, size=(400, 30))
        self.file_name.SetFont(txt_font)
        box.Add(file_txt, 0, wx.ALIGN_CENTER_HORIZONTAL)
        box.Add(self.file_name, 0, wx.ALIGN_CENTER_HORIZONTAL)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # buttons
        self.create_file = wx.Button(self, -1, "create file")  # edit file btn
        self.back = wx.Button(self, -1, "back")  # add file in btn
        self.create_file.SetSize((100, 50))
        self.back.SetSize((100, 50))

        # buttons settings
        self.create_file.SetFont(btn_font)
        self.back.SetFont(btn_font)
        self.back.SetForegroundColour(wx.Colour(255, 255, 255))
        self.create_file.SetBackgroundColour((255, 255, 255, 255))
        self.back.SetBackgroundColour((0, 0, 0, 0))

        # adding btns
        btn_sizer.Add(self.create_file, 0)
        btn_sizer.AddSpacer(200)
        btn_sizer.Add(self.back, 0)
        box.AddSpacer(100)

        # adding btns
        box.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # alignments
        self.SetSizer(box)


class EditFile(wx.Panel):
    """edit file panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.usernames = []    # list of connected users
        # strips dictionary = {strip name : list of widgets}
        self.strips = {}
        # {strip name : [is_editing, username}
        self.strip_edit = {}

        # vertical sizer
        box = wx.BoxSizer(wx.VERTICAL)

        # screen width and height for sizing
        screenWidth, screenHeight = wx.DisplaySize()

        self.SetBackgroundColour('#D14081')  # setting background color

        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        txt_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font
        txt2_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, underline=True)  # font

        # creating buttons
        self.add_strip = wx.Button(self, label="add strip", size=(150, 50))
        self.add_strip.SetBackgroundColour('#40d190')
        self.add_strip.SetFont(btn_font)
        # self.back = wx.Button(self, label="back", size=(100, 50))  # back btn
        # self.back.SetBackgroundColour((0, 0, 0, 0))
        # self.back.SetFont(btn_font)
        # self.back.SetForegroundColour(wx.Colour(255, 255, 255))
        self.play_audio = wx.Button(self, label="play audio", size=(150, 50))
        self.play_audio.SetBackgroundColour('#40d190')
        self.play_audio.SetFont(btn_font)
        self.save_file = wx.Button(self, label="save file", size=(150, 50))
        self.save_file.SetBackgroundColour('#40d190')
        self.save_file.SetFont(btn_font)

        # edit panel
        hoz_edit_sizer = wx.BoxSizer(wx.HORIZONTAL)  # horizontal sizer
        self.edit_panel = wx.Panel(self, size=(int(screenWidth*0.35), int(screenHeight*0.75)), style=wx.NO_BORDER)
        self.edit_panel.SetBackgroundColour('#5A5A5A')  # setting background color
        hoz_edit_sizer.AddSpacer(20)
        hoz_edit_sizer.Add(self.edit_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # real edit panel
        hoz_real_edit_sizer = wx.BoxSizer(wx.VERTICAL)  # vertical sizer
        self.edit_edit_panel = wx.Panel(self.edit_panel, size=(int(screenWidth * 0.3)
                                                    , int(screenHeight * 0.5625)), style=wx.NO_BORDER)
        self.edit_edit_panel.SetBackgroundColour('#5A5A5A')  # setting background color

        # edit strip panel widgets
        volume = wx.StaticText(self.edit_edit_panel, label="volume:")  # volume
        volume.SetFont(txt2_font)
        self.volume = wx.StaticText(self.edit_edit_panel, label="50%")  # volume
        self.volume.SetFont(txt_font)
        self.volume.SetBackgroundColour('#FFFFFF')  # volume background color
        # volume butons
        plus = wx.Bitmap('plus.png')   # create wx.Bitmap object
        minus = wx.Bitmap('minus.png')   # create wx.Bitmap object
        self.plus = wx.Button(self.edit_edit_panel, size=(30, 30), style=wx.NO_BORDER)
        self.plus.SetBackgroundColour('#5A5A5A')
        self.plus.SetBitmap(plus)  # set bmp as bitmap for button
        self.minus = wx.Button(self.edit_edit_panel, size=(30, 30), style=wx.NO_BORDER)
        self.minus.SetBackgroundColour('#5A5A5A')
        self.minus.SetBitmap(minus)  # set bmp as bitmap for button
        # volume sizer
        volume_sizer = wx.BoxSizer(wx.HORIZONTAL)  # horizontal sizer
        volume_sizer.Add(self.minus, 0, wx.ALIGN_CENTER_HORIZONTAL)
        volume_sizer.AddSpacer(5)
        volume_sizer.Add(self.volume, 0, wx.ALIGN_CENTER_HORIZONTAL)
        volume_sizer.AddSpacer(5)
        volume_sizer.Add(self.plus, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_real_edit_sizer.AddSpacer(10)
        hoz_real_edit_sizer.Add(volume, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_real_edit_sizer.Add(volume_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        # cutting buttons and ctrls
        mili = wx.StaticText(self.edit_edit_panel, label="cut seconds from strip:")  # cut milliseconds
        mili.SetFont(txt2_font)
        self.beginning = wx.TextCtrl(self.edit_edit_panel, size=(100, 30))
        self.beginning.SetFont(txt_font)
        self.end = wx.TextCtrl(self.edit_edit_panel, size=(100, 30))
        self.end.SetFont(txt_font)
        cut_sizer = wx.BoxSizer(wx.HORIZONTAL)  # horizontal sizer
        cut_sizer.Add(self.beginning, 0, wx.ALIGN_CENTER_HORIZONTAL)
        cut_sizer.AddSpacer(150)
        cut_sizer.Add(self.end, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_real_edit_sizer.AddSpacer(20)
        hoz_real_edit_sizer.Add(mili, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_real_edit_sizer.AddSpacer(10)
        hoz_real_edit_sizer.Add(cut_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        # adding cutting buttons
        self.cut_beginning = wx.Button(self.edit_edit_panel, size=(150, 30), style=wx.NO_BORDER, label='cut beginning')
        self.cut_beginning.SetFont(btn_font)
        self.cut_beginning.SetBackgroundColour('#40d190')
        self.cut_end = wx.Button(self.edit_edit_panel, size=(150, 30), style=wx.NO_BORDER, label='cut end')
        self.cut_end.SetFont(btn_font)
        self.cut_end.SetBackgroundColour('#40d190')
        cut_button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # horizontal sizer
        cut_button_sizer.Add(self.cut_beginning, 0, wx.ALIGN_CENTER_HORIZONTAL)
        cut_button_sizer.AddSpacer(100)
        cut_button_sizer.Add(self.cut_end, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_real_edit_sizer.AddSpacer(10)
        hoz_real_edit_sizer.Add(cut_button_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        # move strip
        mov_hoz = wx.BoxSizer(wx.HORIZONTAL)  # horizontal sizer
        start = wx.StaticText(self.edit_edit_panel, label="starting point in seconds")  # starting point
        start.SetFont(txt2_font)
        hoz_real_edit_sizer.AddSpacer(20)
        hoz_real_edit_sizer.Add(start, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.starting_point = wx.TextCtrl(self.edit_edit_panel, size=(80, 30), style=wx.TE_CENTRE)  # input of starting point
        self.starting_point.SetFont(txt_font)
        self.change_start = wx.Button(self.edit_edit_panel, size=(200, 30), style=wx.NO_BORDER,
                                      label='change starting point')
        self.change_start.SetFont(btn_font)
        self.change_start.SetBackgroundColour('#40d190')
        hoz_real_edit_sizer.AddSpacer(10)
        hoz_real_edit_sizer.Add(self.starting_point, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_real_edit_sizer.AddSpacer(10)
        hoz_real_edit_sizer.Add(self.change_start, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # delete strip button
        self.delete = wx.Button(self.edit_edit_panel, size=(120, 40),
                                      label='delete strip')
        self.delete.SetFont(btn_font)
        self.delete.SetBackgroundColour('#FF0000')
        hoz_real_edit_sizer.AddSpacer(100)
        hoz_real_edit_sizer.Add(self.delete, 0, wx.ALIGN_LEFT)

        # seting strip edit panel sizer
        self.edit_edit_panel.SetSizer(hoz_real_edit_sizer)

        # scroller
        self.scroll_vert = wx.BoxSizer(wx.VERTICAL)  # vertical sizer
        hoz_scroll_sizer = wx.BoxSizer(wx.HORIZONTAL)  # vertical sizer
        self.strips_scroller = wx.lib.scrolledpanel.ScrolledPanel(self, -1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER,
                                                      size=(int(screenWidth*0.6), int(screenHeight*0.75)))
        self.strips_scroller.SetBackgroundColour('#5A5A5A')
        self.strips_scroller.SetAutoLayout(1)
        self.strips_scroller.SetupScrolling()
        self.strips_scroller.SetSizer(self.scroll_vert)
        # self.strips_scroller.Bind(wx.EVT_SCROLLWIN, self.handle_scroll)

        # edit panel widgets
        vert_edit_sizer = wx.BoxSizer(wx.VERTICAL)   # sizer for edit panel vertical
        self.strip_name = wx.StaticText(self.edit_panel, label=" ")  # strip name
        self.strip_name.SetFont(txt2_font)
        self.strip_length = wx.StaticText(self.edit_panel, label=" ")     # length of strip
        self.strip_length.SetFont(txt_font)
        self.strip_length.SetForegroundColour(wx.Colour(255, 255, 255))
        vert_edit_sizer.AddSpacer(20)
        # adding strip length and name to sizer
        vert_edit_sizer.Add(self.strip_name, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert_edit_sizer.Add(self.strip_length, 0, wx.ALIGN_CENTER_HORIZONTAL)
        # button to mute
        self.mute = wx.Button(self.edit_panel, label="mute", size=(70, 50))
        self.mute.SetBackgroundColour('#40d190')
        self.mute.SetFont(btn_font)
        # button to edit strip
        self.edit = wx.Button(self.edit_panel, label="edit strip", size=(120, 50))
        self.edit.SetBackgroundColour('#40d190')
        self.edit.SetFont(btn_font)
        edit_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        edit_button_sizer.Add(self.mute, 0, wx.ALIGN_CENTER_HORIZONTAL)
        edit_button_sizer.AddSpacer(20)
        edit_button_sizer.Add(self.edit, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert_edit_sizer.AddSpacer(20)
        vert_edit_sizer.Add(edit_button_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        # adding real edit panel
        vert_edit_sizer.Add(self.edit_edit_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.edit_edit_panel.Hide()

        # scroll horizontal sizer
        hoz_scroll_sizer.Add(self.edit_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_scroll_sizer.AddSpacer(20)
        hoz_scroll_sizer.Add(self.strips_scroller, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hoz_scroll_sizer.AddSpacer(20)

        # adding button
        btn_sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        btn_sizer_top.Add(self.add_strip, 0, wx.RIGHT | wx.ALIGN_RIGHT, int(screenWidth*0.6)-130)
        # btn_sizer_top.Add(self.back, 0, wx.RIGHT | wx.ALIGN_RIGHT, 20)
        box.Add(btn_sizer_top, 0, wx.ALIGN_RIGHT)

        # adding scroll
        box.AddSpacer(20)
        box.Add(hoz_scroll_sizer, 0, wx.ALIGN_RIGHT)

        # # ruller panel
        # self.ruller_panel = Ruller(self)
        # box.AddSpacer(20)
        # box.Add(self.ruller_panel, 0, wx.RIGHT | wx.ALIGN_RIGHT, 20)

        # adding bottom buttons
        btn_sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer_bottom.Add(self.play_audio, 0, wx.RIGHT | wx.ALIGN_RIGHT, int(screenWidth * 0.6) - 300)
        btn_sizer_bottom.Add(self.save_file, 0, wx.RIGHT | wx.ALIGN_RIGHT, 20)
        box.AddSpacer(20)
        box.Add(btn_sizer_bottom, 0, wx.ALIGN_RIGHT)

        # alignments
        self.SetSizer(box)
        self.edit_panel.SetSizer(vert_edit_sizer)

        # hiding edit panel
        self.edit_panel.Hide()

    # def handle_scroll(self, event):
    #     """
    #
    #     :param event:
    #     :return:
    #     """
    #     print('top')
    #     if event.Orientation == wx.SB_HORIZONTAL:
    #         self.ruller_panel.ruller_scroller.Scroll(event.Position, -1)
    #     event.Skip()


# class Ruller(wx.Panel):
#     """edit file panel"""
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#
#         # parent
#         self.parent = parent
#         # screen width and height for sizing
#         screenWidth, screenHeight = wx.DisplaySize()
#
#         # scroller
#         self.scroll_hoz = wx.BoxSizer(wx.HORIZONTAL)  # vertical sizer
#         self.ruller_scroller = wx.lib.scrolledpanel.ScrolledPanel(self, -1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER,
#                                                                   size=(int(screenWidth * 0.6), 50))
#         self.ruller_scroller.SetBackgroundColour('#5A5A5A')
#         self.ruller_scroller.SetAutoLayout(1)
#         self.ruller_scroller.SetupScrolling()
#
#         # ruller button
#         self.ruler = rc.RulerCtrl(self.ruller_scroller, -1, orient=wx.HORIZONTAL, style=wx.SUNKEN_BORDER)
#         self.scroll_hoz.Add(self.ruler, 1, wx.EXPAND, 0)
#
#         self.ruller_scroller.SetAutoLayout(1)
#         self.ruller_scroller.SetupScrolling()
#         self.ruller_scroller.SetSizer(self.scroll_hoz)
#
#         self.ruller_scroller.Bind(wx.EVT_SCROLLWIN, self.handle_scroll)
#
#     def handle_scroll(self, event):
#         """
#
#         :param event:
#         :return:
#         """
#         if event.Orientation == wx.SB_HORIZONTAL:
#             print(f'scroll scroll ', event.Position)
#             self.parent.strips_scroller.Scroll(event.Position, -1)
#         event.Skip()


class AddStrip(wx.Panel):
    """add file strip"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.strip_file = ''    # strip file to upload
        self.strip = ''    # strip name
        box = wx.BoxSizer(wx.VERTICAL)  # vertical sizer

        box.AddSpacer(50)

        # logo
        png = wx.Image('logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # logo image
        self.bitmap = wx.StaticBitmap(self, -1, png, (png.GetWidth(), png.GetHeight()))
        box.Add(self.bitmap, 0, wx.ALIGN_CENTER)
        self.SetBackgroundColour('#D14081')

        # font
        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        txt_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # font

        # text ctrl to fill strip name
        file_txt = wx.StaticText(self, label="enter strip name", style=wx.ALIGN_CENTRE)
        file_txt.SetFont(txt_font)
        self.strip_name = wx.TextCtrl(self, size=(400, 30))
        self.strip_name.SetFont(txt_font)
        box.Add(file_txt, 0, wx.ALIGN_CENTER_HORIZONTAL)
        box.Add(self.strip_name, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # select file button
        self.select_file = wx.Button(self, -1, "choose a file")
        box.Add(self.select_file, 0, wx.ALIGN_CENTER_HORIZONTAL)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # buttons
        self.create_strip = wx.Button(self, -1, "add strip")  # edit file btn
        self.back = wx.Button(self, -1, "back")  # add file in btn
        self.create_strip.SetSize((100, 50))
        self.back.SetSize((100, 50))

        # buttons settings
        self.create_strip.SetFont(btn_font)
        self.back.SetFont(btn_font)
        self.back.SetForegroundColour(wx.Colour(255, 255, 255))
        self.create_strip.SetBackgroundColour((255, 255, 255, 255))
        self.back.SetBackgroundColour((0, 0, 0, 0))

        # adding btns
        btn_sizer.Add(self.create_strip, 0)
        btn_sizer.AddSpacer(200)
        btn_sizer.Add(self.back, 0)
        box.AddSpacer(100)

        # adding btns
        box.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # alignments
        self.SetSizer(box)


class Loading(wx.Panel):
    """add file strip"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        box = wx.BoxSizer(wx.VERTICAL)  # vertical sizer

        self.SetBackgroundColour('#D14081')

        # showing loading widget
        loading = Animation()
        loading.LoadFile('loading.gif')
        ctrl = AnimationCtrl(self, -1, loading)
        ctrl.Play()
        box.Add(ctrl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        # alignments
        self.SetSizer(box)


class Program(wx.Frame):
    """graphic frame contains all panels"""
    def __init__(self, comm):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Program', style=wx.DEFAULT_FRAME_STYLE)
        # client comm
        self.comm = comm
        # file comm
        self.file_comm = None
        # username of client
        self.username = ''
        sizer = wx.BoxSizer()
        self.SetSizer(sizer)
        self.Maximize(True)

        # panels
        self.sign_in_panel = SignIn(self)
        self.log_in_panel = LogIn(self)
        self.home_panel = Home(self)
        self.add_file_panel = AddFile(self)
        self.edit_panel = EditFile(self)
        self.add_strip_panel = AddStrip(self)
        self.loading_panel = Loading(self)

        # log in panel
        sizer.Add(self.log_in_panel, 1, wx.EXPAND)
        self.log_in_panel.log_in.Bind(wx.EVT_BUTTON, self.log_in)
        self.log_in_panel.sign_in.Bind(wx.EVT_BUTTON, self.show_panel_two)

        # sign in panel
        sizer.Add(self.sign_in_panel, 1, wx.EXPAND)
        self.sign_in_panel.sign_in.Bind(wx.EVT_BUTTON, self.sign_in)
        self.sign_in_panel.back.Bind(wx.EVT_BUTTON, self.show_panel_one)

        # home panel
        sizer.Add(self.home_panel, 1, wx.EXPAND)
        self.home_panel.edit_file.Bind(wx.EVT_BUTTON, self.start_editing)
        self.home_panel.add_file.Bind(wx.EVT_BUTTON, self.show_panel_four)

        # add file panel
        sizer.Add(self.add_file_panel, 1, wx.EXPAND)
        self.add_file_panel.back.Bind(wx.EVT_BUTTON, self.show_panel_three)
        self.add_file_panel.create_file.Bind(wx.EVT_BUTTON, self.create_file)

        # edit file panel
        sizer.Add(self.edit_panel, 1, wx.EXPAND)
        self.edit_panel.add_strip.Bind(wx.EVT_BUTTON, self.show_panel_six)
        self.edit_panel.play_audio.Bind(wx.EVT_BUTTON, self.play_audio)
        self.edit_panel.mute.Bind(wx.EVT_BUTTON, self.mute_unmute)
        self.edit_panel.edit.Bind(wx.EVT_BUTTON, self.start_edit_strip)
        self.edit_panel.plus.Bind(wx.EVT_BUTTON, self.inc)
        self.edit_panel.minus.Bind(wx.EVT_BUTTON, self.dec)
        self.edit_panel.cut_beginning.Bind(wx.EVT_BUTTON, self.check_cut_beginning)
        self.edit_panel.cut_end.Bind(wx.EVT_BUTTON, self.check_cut_end)
        self.edit_panel.save_file.Bind(wx.EVT_BUTTON, self.on_save_file)
        self.edit_panel.change_start.Bind(wx.EVT_BUTTON, self.check_change_start)
        self.edit_panel.delete.Bind(wx.EVT_BUTTON, self.delete_strip)
        # self.edit_panel.back.Bind(wx.EVT_BUTTON, self.on_back)

        # add strip panel
        sizer.Add(self.add_strip_panel, 1, wx.EXPAND)
        self.add_strip_panel.create_strip.Bind(wx.EVT_BUTTON, self.request_strip)
        self.add_strip_panel.select_file.Bind(wx.EVT_BUTTON, self.on_choose_file)
        self.add_strip_panel.back.Bind(wx.EVT_BUTTON, self.show_panel_five)

        # loading panel
        sizer.Add(self.loading_panel, 1, wx.EXPAND)

        # hiding panels
        self.sign_in_panel.Hide()
        self.home_panel.Hide()
        self.add_file_panel.Hide()
        self.edit_panel.Hide()
        self.add_strip_panel.Hide()
        self.loading_panel.Hide()

        # pubsubs
        pub.subscribe(self.show_panel_three, "success_login")
        pub.subscribe(self.pop_error, "fail_login")
        pub.subscribe(self.show_panel_three, "success_sign_in")
        pub.subscribe(self.pop_error, "fail_sign_in")
        pub.subscribe(self.set_users, "set_users")
        pub.subscribe(self.pop_error, "user_already_connected")
        pub.subscribe(self.set_files, "set_files")
        pub.subscribe(self.show_panel_five, "open_edit")
        pub.subscribe(self.pop_error, "file_exists")
        pub.subscribe(self.add_user, "add_user")
        pub.subscribe(self.add_file, "add_file")
        pub.subscribe(self.set_file_comm, "file_comm")
        pub.subscribe(self.add_strip, "add_strip")
        pub.subscribe(self.show_panel_loading, "loading")
        pub.subscribe(self.play_audio, "music_stopped")
        pub.subscribe(self.editor_edit, "start_stop_edit")
        pub.subscribe(self.pop_error, "strip_exists")
        pub.subscribe(self.client_strip, "send_strip")
        pub.subscribe(self.show_edit_strip, "edit_strip")
        pub.subscribe(self.pop_error, "strip_occupied")
        pub.subscribe(self.inc, "inc_volume")
        pub.subscribe(self.dec, "dec_volume")
        pub.subscribe(self.cut_beginning, "cut_beginning")
        pub.subscribe(self.cut_end, "cut_end")
        pub.subscribe(self.change_start, "move_strip")
        pub.subscribe(self.delete_strip, "delete_strip")

    def log_in(self, event):
        """
        checking if password and username are not empty
        :return: None
        """
        password = self.log_in_panel.password.GetValue()
        username = self.log_in_panel.username.GetValue()
        if len(password) > 0 and len(username) > 0:
            # sending log in message
            self.comm.send(ClientProtocol.log_in(username, password))
        else:
            self.pop_error("you have to fill in username and password")

        event.Skip()

    def sign_in(self, event):
        """
        checking if password and username are not empty
        :return: None
        """
        password = self.sign_in_panel.password.GetValue()
        username = self.sign_in_panel.username.GetValue()

        # checking username requirements
        if len(password) == 0 or len(username) == 0:
            self.pop_error("you have to fill in username and password")
        elif ',' in username or ';' in username or '|' in username:
            self.pop_error("username cannot contain ',' or ';' or '|'")
        elif len(username) > 20:
            self.pop_error("username can't be longer than 20 characters")
        elif ' ' in username:
            self.pop_error("username can't contain whitespace")
        else:
            # sending sign in message
            self.comm.send(ClientProtocol.sign_in(username, password))
        event.Skip()

    def start_editing(self, event):
        """
        sends start editing message to server
        :return: None
        """
        self.show_panel_loading(None)
        index = self.home_panel.choice_box.GetSelection()
        # checking if list is empty
        if len(self.home_panel.edit_files) == 0:
            self.pop_error('you have no edit files')
        elif index == -1:   # if nothing was selected
            self.pop_error('you have to select a file')
        else:
            # sending to server that we want to edit a file
            self.comm.send(ClientProtocol.start_edit_file(self.home_panel.choice_box.GetString(index)))

        event.Skip()

    def create_file(self, event):
        """
        checking input and sending create file message to server
        :param event: None
        :return: None
        """
        file_name = self.add_file_panel.file_name.GetValue()

        # checking input
        if len(file_name) == 0:
            self.pop_error('you have to fill in file name')
        elif ',' in file_name or ';' in file_name or '|' in file_name:
            self.pop_error("file_name cannot contain ',' or ';' or '|'")
        elif len(self.add_file_panel.choice_box.GetCheckedStrings()) == 0:
            self.pop_error("you have to select users to edit with")
        else:
            # sending create file request to server
            file = file_name + ';' + self.username + ',' + ','.join(self.add_file_panel.choice_box.GetCheckedStrings())
            self.comm.send(ClientProtocol.create_file(file))

    def request_strip(self, event):
        """
        checking add strip input and sending add strip to sever
        :param event: None
        :return: None
        """
        strip_name = self.add_strip_panel.strip_name.GetValue()

        # checking input
        if len(strip_name) == 0:
            self.pop_error('you have to fill in strip name')
        elif ',' in strip_name or ';' in strip_name or '|' in strip_name:
            self.pop_error("strip name cannot contain ',' or ';' or '|'")
        elif len(self.add_strip_panel.strip_file) == 0:
            self.pop_error('you have to select strip file')
        else:
            # sending strip request to server
            self.comm.send(ClientProtocol.strip_name_request(strip_name))

    def client_strip(self):
        """
        sending strip to server
        :return: None
        """
        # showing loading panel
        self.show_panel_loading(None)

        strip_name = self.add_strip_panel.strip_name.GetValue()
        path = self.add_strip_panel.strip_file  # file path

        # sending strip to server
        threading.Thread(target=self.send_strip, args=(strip_name, path,), daemon=True).start()

        # sending client information about strip
        wx.CallAfter(pub.sendMessage, "add_strip_logic", file_path=self.add_strip_panel.strip_file
                     , strip_name=strip_name, starting_point=0.0, volume=0)

    def send_strip(self, strip_name, path):
        """
        :param strip_name: strip name
        :param path: strip file path
        :return:
        """
        # sending strip name
        self.file_comm.send(ClientProtocol.add_strip(strip_name))
        # sending starting point
        self.file_comm.send(ClientProtocol.send_start_time('0.0'))
        # sending volume
        self.file_comm.send(ClientProtocol.send_volume('0'))
        # sending file
        self.file_comm.send_file(path)

    def on_choose_file(self, event):
        wildcard = 'Audio files (*.wav)|*.wav'
        dlg = wx.FileDialog(self, message='Choose an audio file', wildcard=wildcard,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.add_strip_panel.strip_file = dlg.GetPath()     # strip file path
        dlg.Destroy()
        event.Skip()

    def on_save_file(self, event):
        dlg = wx.FileDialog(self, message="Save file", defaultDir="",
                       wildcard="All files (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()     # strip file path
            # telling logic to save file
            wx.CallAfter(pub.sendMessage, "save_file", file_path=path)
        dlg.Destroy()
        event.Skip()

    def set_users(self, users):
        """
        setting users list
        :param users: list of users
        :return: None
        """
        # setting client username
        self.username = users[0]
        self.add_file_panel.usernames = users[1:]
        self.add_file_panel.choice_box.Set(self.add_file_panel.usernames)

    def set_files(self, file_names):
        """
        setting file name
        :param file_names: file names
        :return: None
        """
        self.home_panel.choice_box.Set(file_names)
        self.home_panel.edit_files = file_names

    def add_user(self, username):
        """
        adding user to usernames list
        :param username: username to ass
        :return: None
        """
        self.add_file_panel.usernames.append(username)
        self.add_file_panel.choice_box.Set(self.add_file_panel.usernames)

    def add_file(self, file_name):
        """
        adding filename to files list
        :param file_name: file name
        :return: None
        """
        self.home_panel.edit_files.append(file_name)
        self.home_panel.choice_box.Set(self.home_panel.edit_files)

    def set_file_comm(self, file_comm):
        """
        setting file comm
        :param file_comm: file comm
        :return: None
        """
        self.file_comm = file_comm

    def add_strip(self, strip_name, starting_point, volume, length, flag):
        """
        adding strip to edit panel
        :param strip_name: strip name
        :param starting_point: starting point
        :param volume: volume
        :param length: strip length
        :param flag: strip flag
        :return: None
        """
        # adding strip widget to scroller
        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        strip_btn = wx.Button(self.edit_panel.strips_scroller, label=strip_name, size=(int(length*50), 80), style=wx.NO_BORDER)
        wave = wx.Bitmap('wave.png')  # create wx.Bitmap object
        strip_btn.SetBitmap(wave)
        strip_btn.SetBackgroundColour('#483D8B')
        strip_btn.SetFont(btn_font)
        self.edit_panel.scroll_vert.AddSpacer(20)
        strip_sizer = wx.BoxSizer(wx.HORIZONTAL)
        strip_sizer.AddSpacer(int(starting_point*50))
        strip_sizer.Add(strip_btn, 0, wx.LEFT | wx.ALIGN_LEFT)
        self.edit_panel.scroll_vert.Add(strip_sizer, 0, wx.LEFT | wx.ALIGN_LEFT)
        self.edit_panel.strips_scroller.SetupScrolling()
        # adding widget to strip list
        self.edit_panel.strips[strip_name] = [strip_btn, starting_point, (50+volume), length, False, strip_sizer]
        # binding button
        strip_btn.Bind(wx.EVT_BUTTON, self.show_edit_panel)
        # hiding loading panel
        if flag:
            self.show_panel_five(None)

    def show_edit_panel(self, event):
        """ showing edit panel """
        if self.edit_panel.edit.GetLabel() == 'edit strip':
            button = event.GetEventObject()
            strip = button.GetLabel()   # name of strip
            strip_length = self.edit_panel.strips[strip][3]
            starting_point = self.edit_panel.strips[strip][1]
            muted = self.edit_panel.strips[strip][4]
            # setting widgets
            if self.edit_panel.strip_name.GetLabel() in self.edit_panel.strips.keys():  # changing color
                self.edit_panel.strips[self.edit_panel.strip_name.GetLabel()][0].SetBackgroundColour('#483D8B')
            self.edit_panel.strip_name.SetLabel(strip)
            self.edit_panel.strip_length.SetLabel(f'strip length: {strip_length*1000//1/1000} seconds')
            self.edit_panel.starting_point.SetLabel(str(starting_point * 1000 // 1 / 1000))
            button.SetBackgroundColour('#3D8B48')   # changing to green
            # setting mute button
            if muted:
                # change color of button
                self.edit_panel.mute.SetBackgroundColour('#FF0000')
                # change text
                self.edit_panel.mute.SetLabel('unmute')
            else:
                # change color of button
                self.edit_panel.mute.SetBackgroundColour('#40d190')
                # change text
                self.edit_panel.mute.SetLabel('mute')
            self.edit_panel.edit_panel.Show()
            self.edit_panel.edit_panel.Layout()
            self.edit_panel.Layout()
            self.Layout()
        else:
            if event.GetEventObject().GetLabel() != self.edit_panel.strip_name.GetLabel():
                self.pop_error('you can only edit 1 strip at a time')

    def play_audio(self, event):
        """
        playing audio or stopping audio
        :return: None
        """
        if event:
            button = event.GetEventObject()
            if button.GetLabel() == 'play audio':
                # telling logic to play audio
                wx.CallAfter(pub.sendMessage, "play_music")
                # change color of button
                button.SetBackgroundColour('#FF0000')
                # change text
                button.SetLabel('stop playing')
            else:
                # telling logic to play audio
                wx.CallAfter(pub.sendMessage, "stop_play")
                # change color of button
                button.SetBackgroundColour('#40d190')
                # change text
                button.SetLabel('play audio')
            event.Skip()
        else:
            # change color of button
            self.edit_panel.play_audio.SetBackgroundColour('#40d190')
            # change text
            self.edit_panel.play_audio.SetLabel('play audio')
        self.Layout()

    def mute_unmute(self, event):
        """
        changes mute and unmute
        :return: None
        """
        if self.edit_panel.play_audio.GetLabel() == 'play audio':
            if self.edit_panel.mute.GetLabel() == 'mute':
                # telling logic to mute
                wx.CallAfter(pub.sendMessage, "mute", strip_name=self.edit_panel.strip_name.GetLabel())
                # change color of button
                self.edit_panel.mute.SetBackgroundColour('#FF0000')
                # change text
                self.edit_panel.mute.SetLabel('unmute')
                self.edit_panel.strips[self.edit_panel.strip_name.GetLabel()][4] = True
            else:
                # telling logic to unmute
                wx.CallAfter(pub.sendMessage, "mute", strip_name=self.edit_panel.strip_name.GetLabel())
                # change color of button
                self.edit_panel.mute.SetBackgroundColour('#40d190')
                # change text
                self.edit_panel.mute.SetLabel('mute')
                self.edit_panel.strips[self.edit_panel.strip_name.GetLabel()][4] = False
            self.Layout()
        event.Skip()

    def start_edit_strip(self, event):
        """
        showing edit panel
        :param event: event
        :return: None
        """
        if self.edit_panel.play_audio.GetLabel() == 'play audio':
            strip_name = self.edit_panel.strip_name.GetLabel()
            self.edit_panel.volume.SetLabel(f'{self.edit_panel.strips[strip_name][2]}%')    # volume
            if self.edit_panel.edit.GetLabel() == 'edit strip':
                # telling server that we are editing this strip
                self.comm.send(ClientProtocol.start_edit_strip(strip_name))
            else:
                # sending to server that we want to stop editing
                self.comm.send(ClientProtocol.stop_editing_strip(strip_name))
                # change color of button
                self.edit_panel.edit.SetBackgroundColour('#40d190')
                # change text
                self.edit_panel.edit.SetLabel('edit strip')
                # hiding edit panel
                self.edit_panel.edit_edit_panel.Hide()
                self.edit_panel.edit_panel.Layout()
                self.edit_panel.Layout()
                self.Layout()
        event.Skip()

    def show_edit_strip(self):
        """
        showing edit strip panel
        :return: None
        """
        # change color of button
        self.edit_panel.edit.SetBackgroundColour('#FF0000')
        # change text
        self.edit_panel.edit.SetLabel('stop editing')
        # setting widgets
        strip_name = self.edit_panel.strip_name.GetLabel()
        self.edit_panel.volume.SetLabel(f'{self.edit_panel.strips[strip_name][2]}%')
        # showing editing panel
        self.edit_panel.edit_edit_panel.Show()
        self.edit_panel.edit_edit_panel.Layout()
        self.edit_panel.edit_panel.Layout()
        self.edit_panel.Layout()
        self.Layout()

    def editor_edit(self, strip_name, username, edit):
        """
        setting strip editors
        :param edit: boolean
        :param strip_name: strip name
        :param username: username
        :return: None
        """
        if edit:
            self.edit_panel.strip_edit[strip_name] = username
        else:
            del self.edit_panel.strip_edit[strip_name]

    def inc(self, event):
        """
        enc volume
        :param event: event or strip name
        :return: None
        """
        strip_name = self.edit_panel.strip_name.GetLabel()
        volume = self.edit_panel.strips[strip_name][2]  # volume
        if type(event) != str:
            if self.edit_panel.play_audio.GetLabel() == 'play audio':
                # increasing volume
                if volume < 100:
                    volume += 10
                    # sending to server we want to inc volume
                    self.comm.send(ClientProtocol.inc_volume(self.edit_panel.strip_name.GetLabel()))
                    # telling logic to increase volume
                    wx.CallAfter(pub.sendMessage, "inc", strip_name=self.edit_panel.strip_name.GetLabel())
                    # setting volume in panel
                    self.edit_panel.volume.SetLabel(f'{volume}%')
                    self.edit_panel.edit_edit_panel.Layout()
                    self.edit_panel.edit_panel.Layout()
                    self.edit_panel.Layout()
                    self.Layout()
        else:
            strip_name = event
            volume = self.edit_panel.strips[strip_name][2]  # volume
            volume += 10
        self.edit_panel.strips[strip_name][2] = volume

    def dec(self, event):
        """
        dec volume
        :param event: event or strip name
        :return: None
        """
        strip_name = self.edit_panel.strip_name.GetLabel()
        volume = self.edit_panel.strips[strip_name][2]  # volume
        if type(event) != str:
            if self.edit_panel.play_audio.GetLabel() == 'play audio':
                # increasing volume
                if volume > 0:
                    volume -= 10
                    # sending to server we want to dec volume
                    self.comm.send(ClientProtocol.dec_volume(self.edit_panel.strip_name.GetLabel()))
                    # telling logic to increase volume
                    wx.CallAfter(pub.sendMessage, "dec", strip_name=self.edit_panel.strip_name.GetLabel())
                    # setting volume in panel
                    self.edit_panel.volume.SetLabel(f'{volume}%')
                    self.edit_panel.edit_edit_panel.Layout()
                    self.edit_panel.edit_panel.Layout()
                    self.edit_panel.Layout()
                    self.Layout()
        else:
            strip_name = event
            volume = self.edit_panel.strips[strip_name][2]  # volume
            volume -= 10
        self.edit_panel.strips[strip_name][2] = volume

    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def check_cut_beginning(self, event):
        """
        checking cutting strip from beginning
        :param event: event
        :return: None
        """
        strip_name = self.edit_panel.strip_name.GetLabel()
        cut_time = self.edit_panel.beginning.GetValue()
        if self.is_float(cut_time):
            cut_time = float(cut_time)
            diff = self.edit_panel.strips[strip_name][3] - cut_time
            if cut_time > 0:
                if diff > 0.99:
                    # sending to server to cut strip
                    self.comm.send(ClientProtocol.shorten_start(strip_name, int(cut_time*1000)))
                    # telling logic to cut strip
                    wx.CallAfter(pub.sendMessage, "beginning", strip_name=strip_name, time=int(cut_time*1000))
                    # clearing intctrl
                    self.edit_panel.beginning.SetValue('')
                    # cutting button
                    self.cut_beginning(strip_name, int(cut_time*1000), True)
                else:
                    self.pop_error('you cannot cut this amount from the strip')
        else:
            self.pop_error('invalid input, you can only enter numbers')

    def cut_beginning(self, strip_name, cut_time, flag):
        """
        cutting string from the beginning
        :param flag: flag for button color
        :param strip_name: strip name
        :param cut_time: cut time
        :return: None
        """
        # cutting
        starting_point = self.edit_panel.strips[strip_name][1]  # starting point
        length = self.edit_panel.strips[strip_name][3]  # strip length
        # creating new strip button
        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        strip_btn = wx.Button(self.edit_panel.strips_scroller, label=strip_name,
                              size=(int((length - cut_time / 1000) * 50), 80), style=wx.NO_BORDER)
        wave = wx.Bitmap('wave.png')  # create wx.Bitmap object
        strip_btn.SetBitmap(wave)
        if flag:
            strip_btn.SetBackgroundColour('#3D8B48')
        elif strip_name == self.edit_panel.strip_name.GetLabel():
            strip_btn.SetBackgroundColour('#3D8B48')
        else:
            strip_btn.SetBackgroundColour('#483D8B')
        strip_btn.SetFont(btn_font)
        cut_time /= 1000
        self.edit_panel.strips[strip_name][5].Clear(True)
        self.edit_panel.strips[strip_name][5].AddSpacer(int((starting_point + cut_time) * 50))
        self.edit_panel.strips[strip_name][5].Add(strip_btn, 0, wx.LEFT | wx.ALIGN_LEFT)
        self.edit_panel.strips_scroller.SetupScrolling()
        # adding new button
        self.edit_panel.strips[strip_name][0] = strip_btn
        self.edit_panel.strips[strip_name][1] = starting_point + cut_time
        self.edit_panel.strips[strip_name][3] = length - cut_time
        # setting length widget
        self.edit_panel.strip_length.SetLabel(f'strip length: {(length - cut_time)*1000//1/1000} seconds')
        self.Layout()
        self.edit_panel.Layout()
        self.edit_panel.edit_panel.Layout()
        # binding button
        strip_btn.Bind(wx.EVT_BUTTON, self.show_edit_panel)

    def check_cut_end(self, event):
        """
        checking cutting strip from the end
        :param event: event
        :return: None
        """
        strip_name = self.edit_panel.strip_name.GetLabel()
        cut_time = self.edit_panel.end.GetValue()
        if self.is_float(cut_time):
            cut_time = float(cut_time)
            diff = self.edit_panel.strips[strip_name][3] - cut_time
            if cut_time > 0:
                if diff > 0.99:
                    # sending to server to cut strip
                    self.comm.send(ClientProtocol.shorten_end(strip_name, int(cut_time*1000)))
                    # telling logic to cut strip
                    wx.CallAfter(pub.sendMessage, "end", strip_name=strip_name, time=int(cut_time*1000))
                    # clearing intctrl
                    self.edit_panel.end.SetValue('')
                    # cutting button
                    self.cut_end(strip_name, int(cut_time*1000), True)
                else:
                    self.pop_error('you cannot cut this amount from the strip')
        else:
            self.pop_error('invalid input, you can only enter numbers')

    def cut_end(self, strip_name, cut_time, flag):
        """
        cutting strip from end
        :param strip_name: strip name
        :param cut_time: cut time
        :param flag: flag for color
        :return: None
        """
        # cutting
        starting_point = self.edit_panel.strips[strip_name][1]  # starting point
        length = self.edit_panel.strips[strip_name][3]  # strip length
        # creating new strip button
        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        strip_btn = wx.Button(self.edit_panel.strips_scroller, label=strip_name,
                              size=(int((length - cut_time / 1000) * 50), 80), style=wx.NO_BORDER)
        wave = wx.Bitmap('wave.png')  # create wx.Bitmap object
        strip_btn.SetBitmap(wave)
        if flag:
            strip_btn.SetBackgroundColour('#3D8B48')
        elif strip_name == self.edit_panel.strip_name.GetLabel():
            strip_btn.SetBackgroundColour('#3D8B48')
        else:
            strip_btn.SetBackgroundColour('#483D8B')
        strip_btn.SetFont(btn_font)
        cut_time /= 1000
        self.edit_panel.strips[strip_name][5].Clear(True)
        self.edit_panel.strips[strip_name][5].AddSpacer(int(starting_point * 50))
        self.edit_panel.strips[strip_name][5].Add(strip_btn, 0, wx.LEFT | wx.ALIGN_LEFT)
        self.edit_panel.strips_scroller.SetupScrolling()
        # adding new button
        self.edit_panel.strips[strip_name][0] = strip_btn
        self.edit_panel.strips[strip_name][3] = length - cut_time
        # setting length widget
        self.edit_panel.strip_length.SetLabel(f'strip length: {(length - cut_time)*1000//1/1000} seconds')
        self.Layout()
        self.edit_panel.Layout()
        self.edit_panel.edit_panel.Layout()

        # binding button
        strip_btn.Bind(wx.EVT_BUTTON, self.show_edit_panel)

    def check_change_start(self, event):
        """
        checking if change start input is correct
        :param event: event
        :return: None
        """
        strip_name = self.edit_panel.strip_name.GetLabel()
        starting_point = self.edit_panel.starting_point.GetValue()
        if self.is_float(starting_point):
            starting_point = float(starting_point)
            if starting_point >= 0:
                if starting_point != self.edit_panel.strips[strip_name][1]:
                    # setting graphic
                    self.change_start(strip_name, starting_point, True)
                    # sending to server to move strip
                    self.comm.send(ClientProtocol.move_strip(strip_name, starting_point))
                    # telling logic to cut strip
                    wx.CallAfter(pub.sendMessage, "move", strip_name=strip_name, time=starting_point)
            else:
                self.pop_error('starting point has to be bigger than 0')
                # setting txtctrl
                self.edit_panel.starting_point.SetValue(str(self.edit_panel.strips[strip_name][1]))
        else:
            self.pop_error('invalid input, you can only enter numbers')
            # setting txtctrl
            self.edit_panel.starting_point.SetValue(str(self.edit_panel.strips[strip_name][1]))

    def change_start(self, strip_name, starting_point, flag):
        """
        moving starting point of strip
        :param strip_name: strip name
        :param flag: flag
        :param starting_point: starting point
        :return: None
        """
        length = self.edit_panel.strips[strip_name][3]  # strip length
        # creating new strip button
        btn_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # font
        strip_btn = wx.Button(self.edit_panel.strips_scroller, label=strip_name,
                              size=(int(length*50), 80), style=wx.NO_BORDER)
        wave = wx.Bitmap('wave.png')  # create wx.Bitmap object
        strip_btn.SetBitmap(wave)
        if flag:
            strip_btn.SetBackgroundColour('#3D8B48')
        elif strip_name == self.edit_panel.strip_name.GetLabel():
            strip_btn.SetBackgroundColour('#3D8B48')
        else:
            strip_btn.SetBackgroundColour('#483D8B')
        strip_btn.SetFont(btn_font)
        self.edit_panel.strips[strip_name][5].Clear(True)
        self.edit_panel.strips[strip_name][5].AddSpacer(int(starting_point*50))
        self.edit_panel.strips[strip_name][5].Add(strip_btn, 0, wx.LEFT | wx.ALIGN_LEFT)
        self.edit_panel.strips_scroller.SetupScrolling()
        # adding new button
        self.edit_panel.strips[strip_name][0] = strip_btn
        self.edit_panel.strips[strip_name][1] = starting_point
        # setting starting point text ctrl
        self.edit_panel.starting_point.SetValue(str(starting_point))
        # setting length widget
        self.Layout()
        self.edit_panel.Layout()
        self.edit_panel.edit_panel.Layout()
        # binding button
        strip_btn.Bind(wx.EVT_BUTTON, self.show_edit_panel)

    def delete_strip(self, event):
        """
        deleting strip
        :param event: event
        :return: None
        """
        strip_name = self.edit_panel.strip_name.GetLabel()
        if type(event) == str:
            strip_name = event
        # deleting strip in gui
        if type(event) != str:
            self.edit_panel.edit_edit_panel.Hide()
            self.edit_panel.edit_panel.Hide()
            # change color of button
            self.edit_panel.edit.SetBackgroundColour('#40d190')
            # change text
            self.edit_panel.edit.SetLabel('edit strip')
        self.edit_panel.strips[strip_name][0].Destroy()
        self.edit_panel.scroll_vert.Remove(self.edit_panel.strips[strip_name][5])
        del self.edit_panel.strips[strip_name]
        # running on all strips
        for strip in self.edit_panel.strips.keys():
            self.edit_panel.scroll_vert.Detach(self.edit_panel.strips[strip][5])
        # hiding all strips
        self.edit_panel.scroll_vert.Clear(True)
        # adding strips
        for strip in self.edit_panel.strips.keys():
            self.edit_panel.scroll_vert.AddSpacer(20)
            self.edit_panel.scroll_vert.Add(self.edit_panel.strips[strip][5], 0, wx.LEFT | wx.ALIGN_LEFT)
        self.edit_panel.strips_scroller.SetupScrolling()

        self.Layout()
        self.edit_panel.Layout()
        if type(event) != str:
            # telling client and server to delete strip
            self.comm.send(ClientProtocol.delete_strip(strip_name))
            wx.CallAfter(pub.sendMessage, "delete", strip_name=strip_name)

    def on_back(self, event):
        """
        returns to home panel
        :param event: event
        :return: None
        """
        # deleting all strips
        self.edit_panel.strips.clear()

        # clearing strips in graphic
        self.edit_panel.scroll_vert.Clear(True)

        # returning to home panel
        self.show_panel_three(None)

        # telling client that we disconnected
        wx.CallAfter(pub.sendMessage, "back")
        # sending message to server that we stopped editing
        self.comm.send('5')

    def show_panel_one(self, event):
        """ showing panel 1"""
        self.log_in_panel.Show()
        self.sign_in_panel.Hide()
        self.Layout()
        event.Skip()

    def show_panel_two(self, event):
        """ showing panel 2"""
        self.sign_in_panel.Show()
        self.log_in_panel.Hide()
        self.Layout()
        event.Skip()

    def show_panel_three(self, event):
        """ showing panel 3"""
        self.home_panel.Show()
        self.sign_in_panel.Hide()
        self.log_in_panel.Hide()
        self.add_file_panel.Hide()
        self.edit_panel.Hide()
        self.edit_panel.edit_edit_panel.Hide()
        self.edit_panel.edit_panel.Hide()
        self.Layout()
        if event:
            event.Skip()

    def show_panel_four(self, event):
        """ showing panel 4"""
        self.add_file_panel.Show()
        self.home_panel.Hide()
        self.Layout()
        event.Skip()

    def show_panel_five(self, event):
        """ showing panel 5"""
        self.edit_panel.Show()
        self.add_file_panel.Hide()
        self.home_panel.Hide()
        self.loading_panel.Hide()
        self.add_strip_panel.Hide()
        self.Layout()
        if event:
            event.Skip()

    def show_panel_six(self, event):
        """ showing panel 6"""
        if self.edit_panel.play_audio.GetLabel() == 'play audio':
            # clearing file anf strip name
            self.add_strip_panel.strip = ''
            self.add_strip_panel.strip_file = ''
            # showing and hiding panels
            self.edit_panel.Hide()
            self.add_strip_panel.Show()
            self.Layout()
        if event:
            event.Skip()

    def show_panel_loading(self, event):
        """ showing loading panel"""
        self.loading_panel.Show()
        self.edit_panel.Hide()
        self.add_strip_panel.Hide()
        self.home_panel.Hide()
        self.Layout()
        if event:
            event.Skip()

    def pop_error(self, msg):
        """
        pops error message
        :param msg: error message
        :return: None
        """
        wx.MessageBox(msg, 'Error', wx.OK)


