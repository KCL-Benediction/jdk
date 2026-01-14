#define _JNI_IMPLEMENTATION_
#include <jawt.h>
#include "jni_util.h"

#include "awt.h"
#include "awt_DrawingSurface.h"

/*
 * Declare library specific JNI_Onload entry if static build
 */
DEF_STATIC_JNI_OnLoad

/*
 * Get the AWT native structure.  This function returns JNI_FALSE if
 * an error occurs.
 */
extern "C" _JNI_IMPORT_OR_EXPORT_ jboolean JNICALL JAWT_GetAWT(JNIEnv* env, JAWT* awt)
{
    if (awt == NULL) {
        return JNI_FALSE;
    }

    if (awt->version != JAWT_VERSION_1_3
        && awt->version != JAWT_VERSION_1_4
        && awt->version != JAWT_VERSION_1_7
        && awt->version != JAWT_VERSION_9) {
        return JNI_FALSE;
    }

    awt->GetDrawingSurface = DSGetDrawingSurface;
    awt->FreeDrawingSurface = DSFreeDrawingSurface;
    if (awt->version >= JAWT_VERSION_1_4) {
        awt->Lock = DSLockAWT;
        awt->Unlock = DSUnlockAWT;
        awt->GetComponent = DSGetComponent;
        if (awt->version >= JAWT_VERSION_9) {
            awt->CreateEmbeddedFrame = awt_CreateEmbeddedFrame;
            awt->SetBounds = awt_SetBounds;
            awt->SynthesizeWindowActivation = awt_SynthesizeWindowActivation;
        }
    }

    return JNI_TRUE;
}
