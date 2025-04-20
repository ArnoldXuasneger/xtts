from TTS.api import TTS
import gradio as gr
import tempfile
import os

# Inicializa o modelo TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

def clone_voice(audio_file, text_to_speak, language):
    # Caminho temporário para salvar o áudio gerado
    output_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    output_path = output_file.name
    output_file.close()
    
    # Gera o áudio com a voz clonada
    tts.tts_to_file(
        text=text_to_speak,
        file_path=output_path,
        speaker_wav=audio_file,
        language=language
    )
    
    return output_path

# Interface Gradio
with gr.Blocks() as demo:
    gr.Markdown("# XTTS-v2 Voice Cloning")
    
    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload Voice Sample (5-10 seconds)")
    
    with gr.Row():
        text_input = gr.Textbox(label="Text to Speak", placeholder="Digite o texto para ser falado...")
        language = gr.Dropdown(
            choices=["pt", "en", "es", "fr", "de", "it", "ja", "zh-cn"], 
            value="pt", 
            label="Language"
        )
    
    with gr.Row():
        clone_button = gr.Button("Generate Speech")
    
    with gr.Row():
        output_audio = gr.Audio(label="Generated Speech")
    
    clone_button.click(
        fn=clone_voice,
        inputs=[audio_input, text_input, language],
        outputs=output_audio
    )

# Inicia o servidor
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=False)
