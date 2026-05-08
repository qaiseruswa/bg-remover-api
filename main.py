from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from PIL import Image
import io

app = FastAPI()

# ✅ Lazy load — sirf pehli request par load hoga
_remover = None

def get_remover():
    global _remover
    if _remover is None:
        from rembg import new_session
        _remover = new_session("u2netp")  # ← Chhota model, kam RAM
    return _remover

@app.get("/")
def root():
    return {"status": "Background Remover API is running!"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    from rembg import remove
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents)).convert("RGBA")
    
    # Chhota model use karo
    session = get_remover()
    output_image = remove(input_image, session=session)
    
    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format="PNG")
    output_bytes.seek(0)
    
    return Response(
        content=output_bytes.read(),
        media_type="image/png"
    )