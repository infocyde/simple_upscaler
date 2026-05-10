# pip install streamlit super-image pillow
import streamlit as st
from PIL import Image
from super_image import EdsrModel, ImageLoader
import io
import os

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

st.set_page_config(page_title="AI Image Upscaler", layout="centered")
st.title("🎨 AI Image Upscaler")
st.write("Upscale your images using AI super-resolution.")

st.sidebar.header("Settings")
scale_option = st.sidebar.selectbox("Upscale Factor", [2, 4], index=1)
keep_size = st.sidebar.checkbox("Keep same output size (resize back to original)")

uploaded_file = st.file_uploader("Drag & drop or select an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    input_path = os.path.join("input", uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Original", use_container_width=True)
    st.write(f"Original size: {img.width}×{img.height}")
    
    if st.button("Upscale Image"):
        with st.spinner(f"Upscaling ×{scale_option}... please wait ⏳"):
            # Load model (first run downloads weights)
            model = EdsrModel.from_pretrained(f'eugenesiow/edsr-base', scale=scale_option)
            
            # Prepare image
            inputs = ImageLoader.load_image(img)
            
            # Upscale
            preds = model(inputs)
            
            # Manual tensor to PIL conversion - FIXED
            output = preds.squeeze(0).cpu().detach().clamp(0, 1).numpy()
            output = (output * 255).astype('uint8')
            output = output.transpose(1, 2, 0)  # CHW to HWC
            upscaled = Image.fromarray(output)
            
            if keep_size:
                upscaled = upscaled.resize(img.size, Image.LANCZOS)
            
            output_filename = f"upscaled_x{scale_option}_{uploaded_file.name}"
            output_path = os.path.join("output", output_filename)
            upscaled.save(output_path)
            
            buf = io.BytesIO()
            upscaled.save(buf, format="PNG")
            buf.seek(0)
        
        st.success("✅ Upscaling complete!")
        st.image(upscaled, caption=f"Upscaled ×{scale_option}", use_container_width=True)
        st.write(f"New size: {upscaled.width}×{upscaled.height}")
        
        st.download_button(
            label="💾 Download Upscaled Image",
            data=buf,
            file_name=output_filename,
            mime="image/png"
        )
        
        st.info(f"📁 Input saved to: {input_path}\n📁 Output saved to: {output_path}")
else:
    st.info("👆 Upload an image to begin.")