# Kivy Android Webview 
Kivy Android Webview with native android webview event supports 
To install it your project , just download the folders razzbee and java_classes into your project folders 

in buildozer , set 
```py
android.add_src = java_classes/*.java
```

###Usage 
```py
from kivy.app import App
from razzbee.webviewengine import WebviewEngine  

class browserApp(app):
  
  webviewEngine = None

	#address box 
	address_bar = ObjectProperty(None)
	
	#can Go Back
	can_go_back = BooleanProperty(False)

	#can go forward 
	can_go_forward = BooleanProperty(False)


	def __init__(self,**kwargs):

		super(BrowserScreen,self).__init__(**kwargs)
	    
		Clock.schedule_once(self._on_init_complete)


	#When the constructor has finished proccessing 
	def _on_init_complete(self,*args):

		#address bar 
		self.address_bar = self.ids.address_bar

		self.top_right_nav = self.ids.top_right_nav 

		#lets check if webview object has been instantiated already
		if(self.webviewEngine is not None):
			return True 
		
		webview_pos_y = self.ids.browser_toolbar.height

		contentWin = self.ids.content_window

		contentWinHeight = Window.height - (webview_pos_y + app_config.bottom_toolbar_height)
		 
		print('----!!___WInDOW WIDTH-------',Window.width) 

		#init webview engine 
		self.webviewEngine = WebviewEngine(
								posX=0,
								posY=webview_pos_y,
								width=Window.width,
								height=contentWinHeight
								)
		
		#Add webview engine class as a widget
		contentWin.add_widget(self.webviewEngine)

		#Listen to events 
		self.webviewEngine.bind(on_page_started=self.proccess_on_page_start)
		
		#On on_page_commit_visible
		self.webviewEngine.bind(on_page_commit_visible=self.proccess_on_page_commit_visible)

		self.webviewEngine.bind(on_should_override_url_loading=self.on_should_override_url_loading)



	#proccess back button 
	def proccess_go_back(self):
		
		#if page can go back, then go back 
		if(self.can_go_back == True):
			self.webviewEngine.goBack()

	#Proccess Go Back 
	def proccess_go_forward(self):

		#if can go forward, then go 
		if(self.can_go_forward == True):
			self.webviewEngine.goForward()
	

	#enable disable back and forward button
	def proccess_on_page_start(self,*args,**kwargs):
		
		#change the url to the new url 
		new_url = kwargs.get('url')

		if(new_url is not None):
			self.update_address_bar_url(new_url)


	#proccess on Page Commit visible 
	def proccess_on_page_commit_visible(self,*args,**kwargs):

		#if the webview can go back, update the button
		self.can_go_back = self.webviewEngine.canGoBack()

		#check if it can go forward 
		self.can_go_forward = self.webviewEngine.canGoForward()



	#should_override_url_loading
	def on_should_override_url_loading(self,*args,**kwargs):

		#change the url to the new url 
		new_url = kwargs.get('url')

```
