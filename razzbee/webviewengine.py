from kivy.uix.widget import Widget                                                              
from kivy.clock import Clock                                                                    
from runnable import run_on_ui_thread
from  kivy.event import EventDispatcher 
from jnius import autoclass
from webviewclient import WebviewClient

 
#Load Native Modules 
WebView = autoclass('android.webkit.WebView')                                                   
WebViewClient = autoclass('android.webkit.WebViewClient')                                       
activity = autoclass('org.kivy.android.PythonActivity').mActivity   
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
View = autoclass('android.view.View')



class WebviewEngine(Widget,EventDispatcher): 

	is_visible = True

	_webview_obj = None

	#events 
	_webview_events = ['on_page_started','on_page_finished',
					   'on_received_error','on_page_commit_visible',
					   'on_should_override_url_loading'
					  ]

	 #initialize :D -- Sweet 
	def __init__(self, **kwargs): 
		
		self.webviewWidth = kwargs.get('width') if kwargs.has_key('width') else LayoutParams.MATCH_PARENT

		self.webviewPosX = kwargs.get('posX') if kwargs.has_key('posX') else 0 

		self.webviewPosY = kwargs.get('posY') if kwargs.has_key('posY') else 0

		self.webviewHeight = kwargs.get('height') if kwargs.has_key('height') else LayoutParams.MATCH_PARENT

		#register Events 
		self._register_events()

		super(WebviewEngine, self).__init__(**kwargs)    
		
		Clock.schedule_once(self.create_webview, 0)

	#method for dispatching events 
	def dispatch_event(self,event_name,**kwargs):
		
		#dispatch
		self.dispatch(event_name,**kwargs)
		print('--- Eevent %s dispatched \n' %event_name, kwargs)

	
	#default event handler
	def _event_default_handler(self,**kwargs):
		pass
	 
	#Event registrar 
	def _register_events(self):

		events = self._webview_events

		#loop and register them 
		for event_name in events:

			#create the default handler
			setattr(self,event_name,self._event_default_handler)
			
			#register the event 
			self.register_event_type(event_name)


	#Magic Method to pipe java's webview methods to this class 
	def __getattr__(self,method_name):
		
		print("----%s--- has been called ====" % method_name)
		#else if the method is a webview Obj
		if hasattr(self._webview_obj,method_name):
			
			#create a dummy function 
			call_method = lambda *x: getattr(self._webview_obj,method_name)(*x) 

			#return method 
			return call_method


		else:
			raise Exception("Method %s not define" % method_name)



	@run_on_ui_thread                                                                           
	def create_webview(self,*args):

		#if the webview is created already, skip it 
		if(self._webview_obj):
			return True 

		#if we have reached this point, then mean the webview is not created                                                            
		webview = WebView(activity)   

		settings = webview.getSettings()
		settings.setJavaScriptEnabled(True)
		settings.setUseWideViewPort(True) # enables viewport html meta tags
		settings.setLoadWithOverviewMode(True) # uses viewport
		settings.setSupportZoom(True) # enables zoom
		settings.setBuiltInZoomControls(True) # enables zoom controls

		#set java events 
		webviewClient = WebviewClient(self)                                                                 
		
		webview.setWebViewClient(webviewClient)

		#webview.setWebChromeClient(WebChromeClient)

		#set Postions 
		webview.setX(self.webviewPosX)
		webview.setY(self.webviewPosY)

		#webview.testNum = 12

		activity.addContentView(webview, LayoutParams(self.webviewWidth,self.webviewHeight))

		webview.loadUrl('http://www.google.com')

		self._webview_obj = webview


	#hide - This will hide the webview widget 
	@run_on_ui_thread 
	def hide(self):
		if self._webview_obj is None and self.is_visible == False:
			return False

		self._webview_obj.setVisibility(View.GONE)

