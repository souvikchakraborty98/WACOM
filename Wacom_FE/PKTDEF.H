/* -------------------------------- pktdef.h -------------------------------- */
/* Combined 16 & 32-bit version. */

#ifdef __cplusplus
extern "C" {
#endif	/* __cplusplus */

#ifndef PACKETNAME
	/* if no packet name prefix */
	#define __PFX(x)	x
	#define __IFX(x,y)	x ## y
#else
	/* add prefixes and infixes to packet format names */
	#define __PFX(x)		__PFX2(PACKETNAME,x)
	#define __PFX2(p,x)		__PFX3(p,x)
	#define __PFX3(p,x)		p ## x
	#define __IFX(x,y)		__IFX2(x,PACKETNAME,y)
	#define __IFX2(x,i,y)	__IFX3(x,i,y)
	#define __IFX3(x,i,y)	x ## i ## y
#endif

#define __SFX2(x,s)		__SFX3(x,s)
#define __SFX3(x,s)		x ## s

#define __TAG  	__IFX(tag,PACKET)
#define __TYPES	__PFX(PACKET), * __IFX(P,PACKET), NEAR * __IFX(NP,PACKET), FAR * __IFX(LP,PACKET)

#define __TAGE  	__IFX(tag,PACKETEXT)
#define __TYPESE	__PFX(PACKETEXT), * __IFX(P,PACKETEXT), NEAR * __IFX(NP,PACKETEXT), FAR * __IFX(LP,PACKETEXT)

#define __DATA		(__PFX(PACKETDATA))
#define __MODE		(__PFX(PACKETMODE))
#define __EXT(x)	__SFX2(__PFX(PACKET),x)


typedef struct __TAG {
	#if (__DATA & PK_CONTEXT)
		HCTX			pkContext;
	#endif
	#if (__DATA & PK_STATUS)
		UINT			pkStatus;
	#endif
	#if (__DATA & PK_TIME)
		DWORD			pkTime;
	#endif
	#if (__DATA & PK_CHANGED)
		WTPKT			pkChanged;
	#endif
	#if (__DATA & PK_SERIAL_NUMBER)
		UINT			pkSerialNumber;
	#endif
	#if (__DATA & PK_CURSOR)
		UINT			pkCursor;
	#endif
	#if (__DATA & PK_BUTTONS)
		DWORD			pkButtons;
	#endif
	#if (__DATA & PK_X)
		LONG			pkX;
	#endif
	#if (__DATA & PK_Y)
		LONG			pkY;
	#endif
	#if (__DATA & PK_Z)
		LONG			pkZ;
	#endif
	#if (__DATA & PK_NORMAL_PRESSURE)
		#if (__MODE & PK_NORMAL_PRESSURE)
			/* relative */
			int			pkNormalPressure;
		#else
			/* absolute */
			UINT		pkNormalPressure;
		#endif
	#endif
	#if (__DATA & PK_TANGENT_PRESSURE)
		#if (__MODE & PK_TANGENT_PRESSURE)
			/* relative */
			int			pkTangentPressure;
		#else
			/* absolute */
			UINT		pkTangentPressure;
		#endif
	#endif
	#if (__DATA & PK_ORIENTATION)
		ORIENTATION		pkOrientation;
	#endif
	#if (__DATA & PK_ROTATION)
		ROTATION		pkRotation; /* 1.1 */
	#endif

#ifndef NOWTEXTENSIONS
	/* extensions begin here. */
	#if (__EXT(FKEYS) == PKEXT_RELATIVE) || (__EXT(FKEYS) == PKEXT_ABSOLUTE)
		UINT			pkFKeys;
	#endif
	#if (__EXT(TILT) == PKEXT_RELATIVE) || (__EXT(TILT) == PKEXT_ABSOLUTE)
		TILT			pkTilt;
	#endif
#endif

} __TYPES ;

#ifndef NOWTEXTENSIONS
typedef struct __TAGE {
	EXTENSIONBASE	pkBase;

	#if (__EXT(EXPKEYS) == PKEXT_RELATIVE) || (__EXT(EXPKEYS) == PKEXT_ABSOLUTE)
		EXPKEYSDATA pkExpKeys; /* 1.4 */
	#endif
	#if (__EXT(TOUCHSTRIP) == PKEXT_RELATIVE) || (__EXT(TOUCHSTRIP) == PKEXT_ABSOLUTE)
		SLIDERDATA	pkTouchStrip; /* 1.4 */
	#endif
	#if (__EXT(TOUCHRING) == PKEXT_RELATIVE) || (__EXT(TOUCHRING) == PKEXT_ABSOLUTE)
		SLIDERDATA	pkTouchRing; /* 1.4 */
	#endif

} __TYPESE ;
#endif

#undef PACKETNAME
#undef __TAG
#undef __TAGE
#undef __TAG2
#undef __TYPES
#undef __TYPESE
#undef __TYPES2
#undef __DATA
#undef __MODE
#undef __PFX
#undef __PFX2
#undef __PFX3
#undef __IFX
#undef __IFX2
#undef __IFX3
#undef __SFX2
#undef __SFX3

#ifdef __cplusplus
}
#endif	/* __cplusplus */
