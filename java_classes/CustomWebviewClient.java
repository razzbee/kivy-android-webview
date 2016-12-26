package com.razzbee.WebviewEngine;

import android.webkit.WebView;
import android.view.View;
import android.webkit.WebViewClient;
import java.lang.String;
import 	android.graphics.Bitmap;


//main class
public class CustomWebviewClient extends WebViewClient{

//listener must be the interface 
CustomWebviewClientInterface callbackListener;


//constructor 
public CustomWebviewClient(CustomWebviewClientInterface callbackListener){
    super();
    this.callbackListener = callbackListener;
}

@Override
public boolean shouldOverrideUrlLoading(WebView view, String url){
	this.callbackListener.shouldOverrideUrlLoading(view,url);
	return false;
}


@Override
public void onPageStarted(WebView view, String url, Bitmap favicon){
 	this.callbackListener.onPageStarted(view,url,favicon);
 }


@Override
public void onPageFinished(WebView view, String url){
 	this.callbackListener.onPageFinished(view,url);
}


public void onPageCommitVisible(WebView view, String url){
 	this.callbackListener.onPageCommitVisible(view,url);
}


@Override
public void onReceivedError(WebView view,  int errorCode, String description, String failingUrl){
 	this.callbackListener.onReceivedError(view, errorCode, description, failingUrl);
}



}//end class 