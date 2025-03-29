import streamlit as st
import requests
import datetime

# ---------- CONFIG ----------
API_KEY = "TU_API_KEY_AQUI"  # reemplaza esto con tu clave de OpenWeather
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ---------- FUNCIONES ----------
def obtener_clima(ciudad):
    params = {
        'q': ciudad + ",PE",
        'appid': API_KEY,
        'units': 'metric',
        'cnt': 16  # 3 días (cada 3 horas x 8 lecturas/día)
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analizar_alertas(data, cultivo):
    lluvia_detectada = False
    helada_detectada = False

    for entrada in data['list']:
        temp_min = entrada['main']['temp_min']
        lluvia = entrada.get('rain', {}).get('3h', 0)

        if lluvia >= 1.0:
            lluvia_detectada = True
        if temp_min < 4:
            helada_detectada = True

    alertas = []
    if lluvia_detectada:
        alertas.append("🌧️ Alerta de lluvia. Se recomienda proteger o posponer cosecha.")
    if helada_detectada:
        alertas.append("❄️ Alerta de helada. Evalúe medidas de protección para el cultivo.")

    if not alertas:
        alertas.append("✅ No se detectan condiciones climáticas adversas en los próximos días.")

    return alertas

# ---------- INTERFAZ STREAMLIT ----------
st.title("🌱 Agro-IA - Clima Inteligente para Agricultores")

ciudad = st.text_input("📍 Ingresa tu ciudad o distrito:", "Ayacucho")
cultivo = st.selectbox("🌾 Selecciona tu cultivo:", ["Papa", "Maíz", "Cebolla", "Otro"])

if st.button("🔍 Analizar clima"):
    clima_data = obtener_clima(ciudad)

    if clima_data:
        st.success("✅ Datos climáticos obtenidos correctamente.")
        alertas = analizar_alertas(clima_data, cultivo)

        st.subheader("🔔 Recomendaciones para los próximos días:")
        for alerta in alertas:
            st.write(alerta)
    else:
        st.error("⚠️ No se pudo obtener el clima. Verifica el nombre de la ciudad o tu conexión.")
