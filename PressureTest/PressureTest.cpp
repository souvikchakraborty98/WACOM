/*----------------------------------------------------------------------------s
	NAME
		PressureTest.cpp

	AUTHORS
		Souvik Chakraborty,2019   
		Souhardya Moulik,2019
---------------------------------------------------------------------------- */

#include "stdafx.h"
#include <windows.h>

#define GET_X_LPARAM(lp)                        ((int)(short)LOWORD(lp))
#define GET_Y_LPARAM(lp)                        ((int)(short)HIWORD(lp))

#include "msgpack.h"
#include "wintab.h"
#define PACKETDATA	(PK_X | PK_Y | PK_BUTTONS | PK_NORMAL_PRESSURE)
#define PACKETMODE	PK_BUTTONS
#include "pktdef.h"
#include "Utils.h"
#include "PressureTest.h"
#include <iostream>
#include <fstream>


#define MAX_LOADSTRING 100

//////////////////////////////////////////////////////////////////////////////
// Global Variables:
HINSTANCE hInst;								// current instance
TCHAR szTitle[MAX_LOADSTRING];					// The title bar text
TCHAR szWindowClass[MAX_LOADSTRING];			// the main window class name

char* gpszProgramName = "PressureTest";
static LOGCONTEXT	glogContext = {0};

//////////////////////////////////////////////////////////////////////////////
// Forward declarations of functions included in this code module:
ATOM				MyRegisterClass(HINSTANCE hInstance);
BOOL				InitInstance(HINSTANCE, int);
LRESULT CALLBACK	WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK	About(HWND, UINT, WPARAM, LPARAM);

HCTX static NEAR TabletInit(HWND hWnd);
void Cleanup( void );

//////////////////////////////////////////////////////////////////////////////
int APIENTRY _tWinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPTSTR    lpCmdLine,
                     int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);

 	// TODO: Place code here.
	MSG msg;
	HACCEL hAccelTable;

	// Initialize global strings
	LoadString(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
	LoadString(hInstance, IDC_PRESSURETEST, szWindowClass, MAX_LOADSTRING);
	MyRegisterClass(hInstance);

	// Perform application initialization:
	if (!InitInstance (hInstance, nCmdShow))
	{
		return FALSE;
	}

	hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_PRESSURETEST));

	// Main message loop:
	while (GetMessage(&msg, NULL, 0, 0))
	{
		if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}

	// Return Wintab resources.
	Cleanup();

	return (int) msg.wParam;
}


//////////////////////////////////////////////////////////////////////////////
//
//  FUNCTION: MyRegisterClass()
//
//  PURPOSE: Registers the window class.
//
//  COMMENTS:
//
//    This function and its usage are only necessary if you want this code
//    to be compatible with Win32 systems prior to the 'RegisterClassEx'
//    function that was added to Windows 95. It is important to call this function
//    so that the application will get 'well formed' small icons associated
//    with it.
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASSEX wcex;

	wcex.cbSize = sizeof(WNDCLASSEX);

	wcex.style			= CS_HREDRAW | CS_VREDRAW;
	wcex.lpfnWndProc	= WndProc;
	wcex.cbClsExtra		= 0;
	wcex.cbWndExtra		= 0;
	wcex.hInstance		= hInstance;
	wcex.hIcon			= LoadIcon(hInstance, MAKEINTRESOURCE(IDI_PRESSURETEST));
	wcex.hCursor		= LoadCursor(NULL, IDC_ARROW);
   wcex.hbrBackground	= (HBRUSH)(COLOR_APPWORKSPACE + 1);
	wcex.lpszMenuName	= MAKEINTRESOURCE(IDC_PRESSURETEST);
	wcex.lpszClassName	= szWindowClass;
	wcex.hIconSm		= LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

	return RegisterClassEx(&wcex);
}

//////////////////////////////////////////////////////////////////////////////
//
//   FUNCTION: InitInstance(HINSTANCE, int)
//
//   PURPOSE: Saves instance handle and creates main window
//
//   COMMENTS:
//
//        In this function, we save the instance handle in a global variable and
//        create and display the main program window.
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
	HWND hWnd;

	hInst = hInstance; // Store instance handle in our global variable

	if ( !LoadWintab( ) )
	{
		ShowError( "Wintab not available" );
		return FALSE;
	}

	/* check if WinTab available. */
	if (!gpWTInfoA(0, 0, NULL)) 
	{
		ShowError( "Come'on Man! WinTab Services Not Available." );
		return FALSE;
	}

	hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
		CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, NULL, NULL, hInstance, NULL);
	

	if (!hWnd)
	{
		return FALSE;
	}
	ShowWindow(hWnd, SW_SHOWMAXIMIZED);
	//ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);

	return TRUE;
}


//////////////////////////////////////////////////////////////////////////////
//
//  FUNCTION: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  PURPOSE:  Processes messages for the main window.
//
//  WM_COMMAND	- process the application menu
//  WM_PAINT	- Paint the main window
//  WM_DESTROY	- post a quit message and return
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	int wmId, wmEvent;
	HDC hdc;

	static HCTX hCtx = NULL;
	static POINT ptOld, ptNew;
	static UINT prsOld, prsNew;
	static RECT rcClient;
	PAINTSTRUCT psPaint;
	PACKET pkt;
	BOOL fHandled = TRUE;
	LRESULT lResult = 0L;
	static int xMousePos = 0;
	static int yMousePos = 0;
	TCHAR text[5]= { '\0' };
	TCHAR text1[5]= { '\0' };
	TCHAR text2[10]= { '\0' };
	std::ofstream myfile1;
	std::ofstream myfile;
	

	switch (message)
	{
	case WM_CREATE:
		hCtx = TabletInit(hWnd);
		if (!hCtx) 
		{
			ShowError("Could Not Open Tablet Context.");
			SendMessage(hWnd, WM_DESTROY, 0, 0L);
		}
		
		break;

	case WM_MOVE:
	case WM_SIZE:
		GetClientRect(hWnd, &rcClient);
		InvalidateRect(hWnd, NULL, TRUE);
		break;

	case WM_COMMAND:
		wmId    = LOWORD(wParam);
		wmEvent = HIWORD(wParam);
		
		switch (wmId)
		{
		case IDM_ABOUT:
			DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
			break;
		case IDM_EXIT:
			DestroyWindow(hWnd);
			break;
		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
		}
		break;

		case WM_PAINT:
		if (hdc = BeginPaint(hWnd, &psPaint)) 
		{
			RECT clientRect;
			POINT scrPoint = {ptNew.x, ptNew.y};
			ScreenToClient(hWnd, &scrPoint);

			GetClientRect(hWnd, &clientRect);
			

			// Draw horizontal line of cross.
			PatBlt(hdc, rcClient.left, scrPoint.y,
				rcClient.right, 1, DSTINVERT);

			// Draw vertical line of cross.
			PatBlt(hdc, scrPoint.x, rcClient.top,
				1, rcClient.bottom, DSTINVERT);

			// Draw ellipse at cross intersection.
		//	Ellipse(hdc, scrPoint.x - prsNew, scrPoint.y - prsNew,
		//		scrPoint.x + prsNew, scrPoint.y + prsNew);
			
			

			_stprintf(text2, _T("%d"), prsNew);
			myfile.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/pressuredata.csv");
			myfile << "Pressure Data\n";
			myfile << text2;
			myfile << ",\n";
			myfile.close();
			
			TextOut(hdc, 100, 20, text2, ARRAYSIZE(text2));
			EndPaint(hWnd, &psPaint);
			
		}
		break;

	case WM_DESTROY:
      if (hCtx)
      {
		   gpWTClose(hCtx);
      }
		PostQuitMessage(0);
		break;

	case WM_MOUSEMOVE:
			xMousePos = GET_X_LPARAM(lParam);
			yMousePos = GET_Y_LPARAM(lParam);
			// Obtain the window's client rectangle 
		//	int temp = xMousePos;
			//int temp1 = yMousePos;
			//int c1 = 0;
		//	int c2 = 0;
			//while (temp > 0)
		//	{
			//	temp = temp / 10;
				//c1++;
			//}

			//while (temp1 > 0)
			//{
				//temp1 = temp1 / 10;
			//	c2++;
			//}
			


			GetClientRect(hWnd, &rcClient);
			hdc = BeginPaint(hWnd, &psPaint);
			
			

			_stprintf(text, _T("%d"), xMousePos);
			_stprintf(text1, _T("%d"), yMousePos);
			
			myfile1.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/coordinatedata.csv");
			myfile1 << "Pressure Data\n";
			myfile1 << text;
			myfile1 << ",";
			myfile1 << text1;
			myfile1 << ",\n";
			myfile1.close();
			
			TextOut(hdc, rcClient.left, rcClient.top, text, ARRAYSIZE(text));
			TextOut(hdc, 100, 0, text1, ARRAYSIZE(text1));
			EndPaint(hWnd, &psPaint);		break;

	case WT_PACKET:
		
		if (gpWTPacket((HCTX)lParam, wParam, &pkt))  
		{
			if (HIWORD(pkt.pkButtons)==TBN_DOWN)                   
			{
				MessageBeep(0);

			}
			ptOld = ptNew;
			prsOld = prsNew;

			ptNew.x = pkt.pkX;
			ptNew.y = pkt.pkY;

			prsNew = pkt.pkNormalPressure;

			if (ptNew.x != ptOld.x ||
				ptNew.y != ptOld.y ||
				prsNew != prsOld) 
			{
				InvalidateRect(hWnd, NULL, TRUE);
			}
		}
		break;

	case WM_ACTIVATE:
		if (GET_WM_ACTIVATE_STATE(wParam, lParam))
      {
			InvalidateRect(hWnd, NULL, TRUE);
      }

		/* if switching in the middle, disable the region */
		if (hCtx) 
      {
			gpWTEnable(hCtx, GET_WM_ACTIVATE_STATE(wParam, lParam));
			if (hCtx && GET_WM_ACTIVATE_STATE(wParam, lParam))
         {
				gpWTOverlap(hCtx, TRUE);
         }
		}
		break;

	default:
		return DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}

//////////////////////////////////////////////////////////////////////////////
// Message handler for about box.
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
	UNREFERENCED_PARAMETER(lParam);
	switch (message)
	{
	case WM_INITDIALOG:
		return (INT_PTR)TRUE;

	case WM_COMMAND:
		if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
		{
			EndDialog(hDlg, LOWORD(wParam));
			return (INT_PTR)TRUE;
		}
		break;
	}
	return (INT_PTR)FALSE;
}

///////////////////////////////////////////////////////////////////////////////
HCTX static NEAR TabletInit(HWND hWnd)
{
	HCTX hctx = NULL;
	UINT wDevice = 0;
	UINT wExtX = 0;
	UINT wExtY = 0;
	UINT wWTInfoRetVal = 0;
	AXIS TabletX = {0};
	AXIS TabletY = {0};

	// Set option to move system cursor before getting default system context.
	glogContext.lcOptions |= CXO_SYSTEM;

	// Open default system context so that we can get tablet data
	// in screen coordinates (not tablet coordinates).
	wWTInfoRetVal = gpWTInfoA(WTI_DEFSYSCTX, 0, &glogContext);
	WACOM_ASSERT( wWTInfoRetVal == sizeof( LOGCONTEXT ) );

	WACOM_ASSERT( glogContext.lcOptions & CXO_SYSTEM );

	// modify the digitizing region
	wsprintf(glogContext.lcName, "PrsTest Digitizing %x", hInst);

	// We process WT_PACKET (CXO_MESSAGES) messages.
	glogContext.lcOptions |= CXO_MESSAGES;

	// What data items we want to be included in the tablet packets
	glogContext.lcPktData = PACKETDATA;

	// Which packet items should show change in value since the last
	// packet (referred to as 'relative' data) and which items
	// should be 'absolute'.
	glogContext.lcPktMode = PACKETMODE;

	// This bitfield determines whether or not this context will receive
	// a packet when a value for each packet field changes.  This is not
	// supported by the Intuos Wintab.  Your context will always receive
	// packets, even if there has been no change in the data.
	glogContext.lcMoveMask = PACKETDATA;

	// Which buttons events will be handled by this context.  lcBtnMask
	// is a bitfield with one bit per button.
	glogContext.lcBtnUpMask = glogContext.lcBtnDnMask;

	// Set the entire tablet as active
	wWTInfoRetVal = gpWTInfoA( WTI_DEVICES + 0, DVC_X, &TabletX );
	WACOM_ASSERT( wWTInfoRetVal == sizeof( AXIS ) );

	wWTInfoRetVal = gpWTInfoA( WTI_DEVICES, DVC_Y, &TabletY );
	WACOM_ASSERT( wWTInfoRetVal == sizeof( AXIS ) );

	glogContext.lcInOrgX = 0;
	glogContext.lcInOrgY = 0;
	glogContext.lcInExtX = TabletX.axMax;
	glogContext.lcInExtY = TabletY.axMax;

	// Guarantee the output coordinate space to be in screen coordinates.  
	glogContext.lcOutOrgX = GetSystemMetrics( SM_XVIRTUALSCREEN );
	glogContext.lcOutOrgY = GetSystemMetrics( SM_YVIRTUALSCREEN );
	glogContext.lcOutExtX = GetSystemMetrics( SM_CXVIRTUALSCREEN ); //SM_CXSCREEN );

	// In Wintab, the tablet origin is lower left.  Move origin to upper left
	// so that it coincides with screen origin.
	glogContext.lcOutExtY = -GetSystemMetrics( SM_CYVIRTUALSCREEN );	//SM_CYSCREEN );

	// Leave the system origin and extents as received:
	// lcSysOrgX, lcSysOrgY, lcSysExtX, lcSysExtY

	// open the region
	// The Wintab spec says we must open the context disabled if we are 
	// using cursor masks.  
	hctx = gpWTOpenA( hWnd, &glogContext, FALSE );

	WacomTrace("HCTX: %i\n", hctx);

	return hctx;
}

///////////////////////////////////////////////////////////////////////////////
void Cleanup( void )
{
	UnloadWintab( );
}
