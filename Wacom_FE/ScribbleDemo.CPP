/*----------------------------------------------------------------------------s
	NAME
		ScribbleDemo.cpp
		Modified to work for Wacom Featture Extractor App
		By Souvik Chakraborty,2019

        Please do not remove auto-generated/informative comments
---------------------------------------------------------------------------- */

#include <windows.h>
#include <windowsx.h>
#include "msgpack.h"
#include "wintab.h"
#define PACKETDATA	(PK_X | PK_Y | PK_BUTTONS | PK_NORMAL_PRESSURE)
#define PACKETMODE	PK_BUTTONS
#include "pktdef.h"
#include "Utils.h"
#include "ScribbleDemo.h"
#include <vector>
#include <map>
#include <tchar.h>
#include <sstream>
#include <iostream>
#include <fstream>
using namespace std;
std::ofstream myfile1;
std::ofstream myfile;

HINSTANCE hInst = NULL;

///////////////////////////////////////////////////////////////////////////////
// Hold tablet-specific properties used when responding to tablet data packets.
//
typedef struct 
{
	int		maxPressure;
	COLORREF	penColor;
	char		name[32];
} TabletInfo;


///////////////////////////////////////////////////////////////////////////////
// Cache all opened contexts.  
// This will allow us to close them when the window closes down.
//
std::map<HCTX, TabletInfo> gContextMap;


///////////////////////////////////////////////////////////////////////////////
// Rotate through these colors for all tablets.
//
typedef enum
{
	PenColorRed,
	PenColorGreen,
	PenColorBlue,

	MAX_PEN_COLOR
} EPenColor;

EPenColor gNextPenColor = PenColorBlue;

///////////////////////////////////////////////////////////////////////////////
// Global variables
//
char* gpszProgramName = "Wacom Feature Extractor";

static int gnOpenContexts = 0;
static int gnAttachedDevices = 0;

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow);
BOOL InitApplication(HINSTANCE hInstance);

///////////////////////////////////////////////////////////////////////////////
int PASCAL WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	MSG msg;

	if (!hPrevInstance)
	if (!InitApplication(hInstance))
		return (FALSE);

	/* Perform initializations that apply to a specific instance */

	if (!InitInstance(hInstance, nCmdShow))
	{
		return (FALSE);
	}

	/* Acquire and dispatch messages until a WM_QUIT message is received. */

	while (GetMessage(&msg, NULL, 0, 0))
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	// Return Wintab resources.
	Cleanup();

	return (msg.wParam);
}



///////////////////////////////////////////////////////////////////////////////
BOOL InitApplication(HINSTANCE hInstance)
{
	WNDCLASS  wc;

	/* Fill in window class structure with parameters that describe the       */
	/* main window.                                                           */

	wc.style = 0;
	wc.lpfnWndProc = MainWndProc;

	wc.cbClsExtra = 0;
	wc.cbWndExtra = 0;
	wc.hInstance = hInstance;
	wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground = (HBRUSH)(COLOR_APPWORKSPACE + 1);
	wc.lpszMenuName =  "ScribbleDemoMenu";
	wc.lpszClassName = "ScribbleDemoWClass";

	/* Register the window class and return success/failure code. */

	return (RegisterClass(&wc));

}



///////////////////////////////////////////////////////////////////////////////
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
	HWND	hWnd;
	char	buf[50];

	/* Save the instance handle in static variable, which will be used in  */
	/* many subsequence calls from this application to Windows.            */

	hInst = hInstance;

	if ( !LoadWintab( ) )
	{
		ShowError( "Wintab not available" );
		return FALSE;
	}

	/* check if WinTab available. */
	if (!gpWTInfoA(0, 0, NULL)) 
	{
		ShowError( "WinTab Services Not Available." );
		return FALSE;
	}

	/* Create a main window for this application instance.  */

	wsprintf(buf, "%s", gpszProgramName);
	hWnd = CreateWindow(
		"ScribbleDemoWClass",
		buf,
		WS_OVERLAPPEDWINDOW,
		CW_USEDEFAULT,
		CW_USEDEFAULT,
		CW_USEDEFAULT,
		CW_USEDEFAULT,
		NULL,
		NULL,
		hInstance,
		NULL
	);


	/* If window could not be created, return "failure" */

	if (!hWnd)
	{
		ShowError( "Could not create window!");
		return (FALSE);
	}
	myfile.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/pressuredata.csv", ios::app);
	myfile << "Pressure Data\n";
	myfile.close();
	myfile1.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/coordinatedata.csv", ios::app);
	myfile1 << "Coordinate Data\n";
	myfile1.close();


	/* Make the window visible; update its client area; and return "success" */

	ShowWindow(hWnd, SW_SHOWMAXIMIZED);
	//ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);
	return (TRUE);

}



///////////////////////////////////////////////////////////////////////////////
// Open contexts for all attached tablets.
// Returns true if any tablet(s) configured.
//
BOOL static NEAR OpenTabletContexts(HWND hWnd)
{
	int ctxIndex = 0;
	gnOpenContexts = 0;
	gnAttachedDevices = 0;
	std::stringstream szTabletName;

	gContextMap.clear();

	gpWTInfoA(WTI_INTERFACE, IFC_NDEVICES, &gnAttachedDevices);
	WacomTrace("Number of attached devices: %i\n", gnAttachedDevices);

	// Open/save contexts until first failure to open a context.
	// Note that gpWTInfoA(WTI_STATUS, STA_CONTEXTS, &nOpenContexts);
	// will not always let you enumerate through all contexts.
	do
	{
		LOGCONTEXT lcMine = {0};
		UINT wWTInfoRetVal = 0;
		AXIS TabletX = {0};
		AXIS TabletY = {0};

		AXIS Pressure = {0};

		WacomTrace("Getting info on contextIndex: %i ...\n", ctxIndex);

		int foundCtx = gpWTInfoA(WTI_DDCTXS + ctxIndex, 0, &lcMine);

		if ( foundCtx > 0 )
		{
			lcMine.lcPktData = PACKETDATA;
			lcMine.lcOptions |= CXO_MESSAGES;
			lcMine.lcOptions |= CXO_SYSTEM;
			lcMine.lcPktMode = PACKETMODE;
			lcMine.lcMoveMask = PACKETDATA;
			lcMine.lcBtnUpMask = lcMine.lcBtnDnMask;

			// Set the entire tablet as active
			wWTInfoRetVal = gpWTInfoA( WTI_DEVICES + ctxIndex, DVC_X, &TabletX );
			if (  wWTInfoRetVal != sizeof( AXIS ) )
			{
				WacomTrace("This context should not be opened.\n");
				continue;
			}

			wWTInfoRetVal = gpWTInfoA( WTI_DEVICES + ctxIndex, DVC_Y, &TabletY );

			gpWTInfoA( WTI_DEVICES + ctxIndex, DVC_NPRESSURE, &Pressure );
			WacomTrace("Pressure: %i, %i\n", Pressure.axMin, Pressure.axMax);

			lcMine.lcInOrgX = 0;
			lcMine.lcInOrgY = 0;
			lcMine.lcInExtX = TabletX.axMax;
			lcMine.lcInExtY = TabletY.axMax;

			// Guarantee the output coordinate space to be in screen coordinates.  
			lcMine.lcOutOrgX = GetSystemMetrics( SM_XVIRTUALSCREEN );
			lcMine.lcOutOrgY = GetSystemMetrics( SM_YVIRTUALSCREEN );
			lcMine.lcOutExtX = GetSystemMetrics( SM_CXVIRTUALSCREEN );

			// In Wintab, the tablet origin is lower left.  Move origin to upper left
			// so that it coincides with screen origin.
			lcMine.lcOutExtY = -GetSystemMetrics( SM_CYVIRTUALSCREEN );

			// Leave the system origin and extents as received:
			// lcSysOrgX, lcSysOrgY, lcSysExtX, lcSysExtY

			// Open the context enabled.
			HCTX hCtx = gpWTOpenA(hWnd, &lcMine, TRUE);

			if ( hCtx )
			{
				// Save context
				COLORREF penColor = MAX_PEN_COLOR;

				switch (gNextPenColor)
				{
					case PenColorRed:		penColor = RGB(255,0,0);	gNextPenColor = PenColorGreen; break;
					case PenColorGreen:	penColor = RGB(0,255,0);	gNextPenColor = PenColorBlue; break;
					case PenColorBlue:	penColor = RGB(0,0,255);	gNextPenColor = PenColorRed; break;
					default:
						WACOM_ASSERT( !"Bad ben color" );
				}

				TabletInfo info = { Pressure.axMax, penColor };
				sprintf(info.name, "Tablet: %i\n", ctxIndex);
				gContextMap[hCtx] = info;
				WacomTrace("Opened context: 0x%X for ctxIndex: %i\n", hCtx, ctxIndex);
				gnOpenContexts++;
			}
			else
			{
				WacomTrace("Did NOT open context for ctxIndex: %i\n", ctxIndex);
			}
		}
		else
		{
			WacomTrace("No context info for ctxIndex: %i, bailing out...\n", ctxIndex);
			break;
		}

		ctxIndex++;
	} while (TRUE);

	if ( gnOpenContexts < gnAttachedDevices )
	{
		ShowError("Oops - did not open a context for each attached device");
	}

	{
		std::stringstream szTitle; szTitle.flush();
		szTitle << gpszProgramName << ": #tablet(s) attached: " << gnAttachedDevices;
		SetWindowText(hWnd, szTitle.str().c_str());
	}

	return gnAttachedDevices > 0;
}

///////////////////////////////////////////////////////////////////////////////
// Close all opened tablet contexts.
//
void CloseTabletContexts(void)
{
	// Close all contexts we opened so we don't have them lying around in prefs.
	for (std::map<HCTX, TabletInfo>::iterator it = gContextMap.begin();
			it != gContextMap.end(); ++it)
	{
		HCTX hCtx = it->first;
		WacomTrace("Closing context: 0x%X\n", hCtx);

		gpWTClose(hCtx);
	}

	gContextMap.clear();

	gnOpenContexts = 0;
	gnAttachedDevices = 0;
}

///////////////////////////////////////////////////////////////////////////////
LRESULT FAR PASCAL MainWndProc(HWND hWnd, unsigned message ,WPARAM wParam, LPARAM lParam)
{
	DLGPROC lpProcAbout;
	static POINT ptOld, ptNew;
	static UINT prsOld, prsNew;
	static RECT rcClient;
	static HCTX hctx = NULL;
	PAINTSTRUCT psPaint;
	HDC hDC;
	PACKET pkt;
	BOOL fHandled = TRUE;
	LRESULT lResult = 0L;
	static int xMousePos = 0;
	static int yMousePos = 0;
	TCHAR text[5] = { '\0' };
	TCHAR text1[5] = { '\0' };
	TCHAR text2[10] = { '\0' };
	

	/*myfile.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/pressuredata.csv", ios::app);
	myfile << "Pressure Data\n";
	myfile.close();
	myfile1.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/coordinatedata.csv", ios::app);
	myfile1 << "Coordinate Data\n";
	myfile1.close();*/

	switch (message) 
	{
		case WM_CREATE:
			// Initialize a Wintab context for each connected tablet.
			if ( !OpenTabletContexts(hWnd) )
			{
				ShowError("Oops! No tablets attached. Please plug in device!");
				SendMessage(hWnd, WM_DESTROY, 0, 0L);
			}
			
			break;

		case WM_MOVE:
		case WM_SIZE:
			GetClientRect(hWnd, &rcClient);
			InvalidateRect(hWnd, NULL, TRUE);
			break;

		case WM_COMMAND:
			if (GET_WM_COMMAND_ID(wParam, lParam) == IDM_ABOUT) {
				lpProcAbout = MakeProcInstance(About, hInst);

				DialogBox(hInst, "AboutBox", hWnd, lpProcAbout);

				FreeProcInstance(lpProcAbout);
			}
			else
				fHandled = FALSE;
			break;

		case WM_MOUSEMOVE:
				xMousePos = GET_X_LPARAM(lParam);
				yMousePos = GET_Y_LPARAM(lParam);

				_stprintf(text, _T("%d"), xMousePos);
				_stprintf(text1, _T("%d"), yMousePos);

				myfile1.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/coordinatedata.csv", ios::app);
				myfile1 << text;
				myfile1 << ",";
				myfile1 << text1;
				myfile1 << ",\n";
				myfile1.close();

//				WacomTrace("mousePos: [%i,%i]\n", xMousePos, yMousePos);
			break;

		case WT_PACKET:
			{
				hctx = (HCTX)lParam;

				// Wintab X/Y data is in screen coordinates. These will have to
				// be converted to client coordinates in the WM_PAINT handler.
				if (gpWTPacket(hctx, wParam, &pkt))
				{
					//WacomTrace("Render point for hctx: 0x%X\n", hctx);

					ptOld = ptNew;
					prsOld = prsNew;

					ptNew.x = pkt.pkX;
					ptNew.y = pkt.pkY;

					prsNew = pkt.pkNormalPressure;

					_stprintf(text2, _T("%d"), prsNew);
					myfile.open("C:/Users/Souvik/Documents/classes/PROJECT/Wacom/pressuredata.csv", ios::app);
					myfile << text2;
					myfile << ",\n";
					myfile.close();

					if (ptNew.x != ptOld.x ||
						 ptNew.y != ptOld.y ||
						 prsNew != prsOld) 
					{
						InvalidateRect(hWnd, NULL, FALSE);
					}
				}
				else
				{
					WacomTrace("Oops - got pinged by an unknown context: 0x%X", hctx);
				}
			}
			break;

      case WT_INFOCHANGE:
         {
            int nAttachedDevices = 0;
            gpWTInfoA(WTI_INTERFACE, IFC_NDEVICES, &nAttachedDevices);

            WacomTrace("WT_INFOCHANGE detected; number of connected tablets is now: %i\n", nAttachedDevices);

				if (nAttachedDevices != gnAttachedDevices )
				{
					// kill all current tablet contexts
					CloseTabletContexts();

					// Add some delay to give driver a chance to catch up in configuring
					// to the current attached tablets.  
					// 1 second seems to work - your mileage may vary...
					::Sleep(1000);

					// re-enumerate attached tablets
					OpenTabletContexts(hWnd);
				}

				if ( gnAttachedDevices == 0 )
				{
					ShowError("No tablets found.");
					SendMessage(hWnd, WM_DESTROY, 0, 0L);
				}
         }
         break;

		case WT_PROXIMITY:
			{
				hctx = (HCTX)wParam;

				bool entering = (HIWORD(lParam) != 0);

				if ( entering )
				{
					if ( gContextMap.count(hctx) > 0 )
					{
						TabletInfo info = gContextMap[hctx];

						std::stringstream szTitle;	szTitle.flush();
						szTitle << gpszProgramName << "; #tablet(s) attached: " << gnAttachedDevices << "; drawing on: " << info.name;
						WacomTrace("Tablet name: %s\n", szTitle.str().c_str());
						SetWindowText(hWnd, szTitle.str().c_str());
					}
					else
					{
						WacomTrace("Oops - couldn't find context: 0x%X\n", hctx);
					}
				}
			}
			break;


	//case WM_ACTIVATE:
		//	if (GET_WM_ACTIVATE_STATE(wParam, lParam))
		//		InvalidateRect(hWnd, NULL, TRUE);

		//	/* if switching in the middle, disable the region */
		//	if (hCtx) {
		//		gpWTEnable(hCtx, GET_WM_ACTIVATE_STATE(wParam, lParam));
		//		if (hCtx && GET_WM_ACTIVATE_STATE(wParam, lParam))
		//			gpWTOverlap(hCtx, TRUE);
		//	}
		//	break;

		case WM_DESTROY:
			CloseTabletContexts();

			PostQuitMessage(0);
			break;

		case WM_PAINT:
			if (hDC = BeginPaint(hWnd, &psPaint)) 
			{
				if ( prsNew > 0 )
				{
					HGDIOBJ original = SelectObject(hDC,GetStockObject(DC_PEN));
					int penWidth = (int)(1 + std::floor(10 * (double)prsNew / (double)gContextMap[hctx].maxPressure));

					COLORREF penColor = gContextMap[hctx].penColor;

					HPEN hPen = CreatePen(PS_SOLID,penWidth,penColor);
					SelectObject(hDC, hPen);

					POINT oldPoint = {ptOld.x, ptOld.y};
					POINT newPoint = {ptNew.x, ptNew.y};

					ScreenToClient(hWnd, &oldPoint);
					ScreenToClient(hWnd, &newPoint);

					MoveToEx(hDC, oldPoint.x, oldPoint.y, NULL);
					LineTo(hDC, newPoint.x, newPoint.y);

					DeleteObject(hPen);
					SelectObject(hDC,original);
					EndPaint(hWnd, &psPaint);
				}
			}
			break;

		default:
			fHandled = FALSE;
			break;
	}
	if (fHandled)
		return (lResult);
	else
		return (DefWindowProc(hWnd, message, wParam, lParam));
}



///////////////////////////////////////////////////////////////////////////////
BOOL FAR PASCAL About(HWND hDlg, unsigned message, WPARAM wParam, LPARAM lParam)
{
	switch (message) {
	case WM_INITDIALOG:
		return (TRUE);

	case WM_COMMAND:
		if (GET_WM_COMMAND_ID(wParam, lParam) == IDOK
				|| GET_WM_COMMAND_ID(wParam, lParam) == IDCANCEL) {
		EndDialog(hDlg, TRUE);
		return (TRUE);
		}
		break;
	}
	return (FALSE);
}



///////////////////////////////////////////////////////////////////////////////
// Purpose
//		Release resources we used in this example.
//
void Cleanup( void )
{
	WACOM_TRACE( "Cleanup()\n" );

	UnloadWintab( );
}


