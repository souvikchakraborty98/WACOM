/*----------------------------------------------------------------------------s
	NAME
		ScribbleDemo.h
---------------------------------------------------------------------------- */

#define IDM_ABOUT 100

int PASCAL WinMain(HINSTANCE, HINSTANCE, LPSTR, int);
BOOL InitApplication(HANDLE);
BOOL InitInstance(HANDLE, int);
LRESULT FAR PASCAL MainWndProc(HWND, unsigned, WPARAM, LPARAM);
BOOL FAR PASCAL About(HWND, unsigned, WPARAM, LPARAM);
void Cleanup( void );
