import gradio as gr

# Variáveis globais para controlar o estado da malha
rows, cols = 10, 10
selected_pixel = [-1, -1]  # Coordenadas do pixel selecionado

def update_pixel(x, y):
    global selected_pixel
    # Atualizar o pixel selecionado
    selected_pixel = [int(x), int(y)]
    return generate_grid_html(selected_pixel)

def generate_grid_html(selected):
    grid_html = "<table style=border-collapse: collapse;>"
    for row in range(rows):
        grid_html += "<tr>"
        for col in range(cols):
            color = "green" if [row, col] == selected else "white"
            grid_html += (
                f"<td onclick=clickPixel({row}, {col}) "
                f"style=width: 20px; height: 20px; border: 1px solid black; background-color: {color};></td>"
            )
        grid_html += "</tr>"
    grid_html += "</table>"
    return grid_html

# Função inicial para exibir a malha
def initialize_grid():
    return generate_grid_html(selected_pixel)

# Interface Gradio
with gr.Blocks() as demo:
    html_output = gr.HTML(value=initialize_grid(), elem_id="grid")
    x_input = gr.Textbox(visible=False)
    y_input = gr.Textbox(visible=False)

    # Atualizar o grid quando houver interação
    gr.HTML(value="<script>"
                  "function clickPixel(x, y) {"
                  "   document.getElementById('x_input').value = x;"
                  "   document.getElementById('y_input').value = y;"
                  "   document.getElementById('x_input').dispatchEvent(new Event('input'));"
                  "   document.getElementById('y_input').dispatchEvent(new Event('input'));"
                  "}"
                  "</script>")

    x_input.change(fn=update_pixel, inputs=[x_input, y_input], outputs=html_output)
    y_input.change(fn=update_pixel, inputs=[x_input, y_input], outputs=html_output)

demo.launch()
