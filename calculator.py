from datetime import datetime, timedelta, date
import math

# ============================================================
# 🔧 FUNCIÓN AUXILIAR: CÁLCULO DE DISTRIBUCIÓN MENSUAL
# ============================================================
def calcular_distribucion_mensual(fecha_inicio, duracion_dias):
    if isinstance(fecha_inicio, datetime):
        fecha_inicio = fecha_inicio.date()

    fecha_fin = fecha_inicio + timedelta(days=duracion_dias - 1)

    # Fin del mes de inicio
    if fecha_inicio.month < 12:
        fin_mes = date(fecha_inicio.year, fecha_inicio.month + 1, 1) - timedelta(days=1)
    else:
        fin_mes = date(fecha_inicio.year, 12, 31)

    # Corrección: si todo el tratamiento cae en el mismo mes
    if fecha_inicio.month == fecha_fin.month:
        dias_mes_actual = duracion_dias
        dias_mes_siguiente = 0
    else:
        dias_mes_actual = (fin_mes - fecha_inicio).days + 1
        dias_mes_siguiente = duracion_dias - dias_mes_actual

    return dias_mes_actual, dias_mes_siguiente, fecha_fin

# ============================================================
# 💉 CÁLCULO PARA AMPOLLAS — 1 inyección = 1 ampolla exacta
# ============================================================
def calcular_ampollas(frecuencia_horas, duracion_dias, dosis_inyeccion, volumen_ampolla, fecha_orden, inicio_mismo_dia):
    inyecciones_por_dia = 24 / frecuencia_horas
    total_inyecciones = inyecciones_por_dia * duracion_dias
    total_ampollas = total_inyecciones * dosis_inyeccion

    ampollas_necesarias = math.ceil(total_ampollas / volumen_ampolla)

    fecha_inicio = fecha_orden if inicio_mismo_dia else fecha_orden + timedelta(days=1)
    dias_mes_actual, dias_mes_siguiente, fecha_fin = calcular_distribucion_mensual(fecha_inicio, duracion_dias)

   # Distribución mensual
    inyecciones_mes_actual = round(inyecciones_por_dia * dias_mes_actual, 1)
    inyecciones_mes_siguiente = round(total_inyecciones - inyecciones_mes_actual, 1)

    volumen_mes_actual = round(inyecciones_mes_actual * dosis_inyeccion, 2)
    volumen_mes_siguiente = round(total_ampollas - volumen_mes_actual, 2)

    ampollas_mes_actual = math.ceil(volumen_mes_actual / volumen_ampolla)
    ampollas_mes_siguiente = math.ceil(volumen_mes_siguiente / volumen_ampolla)

    resultados = {
        "Total de inyecciones": round(total_inyecciones, 1),
        "Volumen total (ml)": round(total_ampollas, 2),
        "Ampollas necesarias": ampollas_necesarias,
        "Fecha de inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Fecha de finalización": fecha_fin.strftime("%Y-%m-%d"),
        "Días este mes": dias_mes_actual,
        "Días próximo mes": dias_mes_siguiente,
        "Ampollas este mes": ampollas_mes_actual,
        "Ampollas próximo mes": ampollas_mes_siguiente,
        "Volumen este mes (ml)": volumen_mes_actual,
        "Volumen próximo mes (ml)": volumen_mes_siguiente
    }

    return resultados

# ============================================================
# 💊 CÁLCULO PARA TABLETAS — distribución mensual precisa
# ============================================================
def calcular_tabletas(frecuencia_horas, duracion_dias, dosis_toma, unidades_presentacion, fecha_orden, inicio_mismo_dia):
    tomas_por_dia = 24 / frecuencia_horas
    total_tomas = tomas_por_dia * duracion_dias
    total_tabletas = total_tomas * dosis_toma

    presentaciones_necesarias = math.ceil(total_tabletas / unidades_presentacion)

    fecha_inicio = fecha_orden if inicio_mismo_dia else fecha_orden + timedelta(days=1)
    dias_mes_actual, dias_mes_siguiente, fecha_fin = calcular_distribucion_mensual(fecha_inicio, duracion_dias)

    tabletas_mes_actual = round(dosis_toma * (24 / frecuencia_horas) * dias_mes_actual, 1)
    tabletas_mes_siguiente = round(total_tabletas - tabletas_mes_actual, 1)

    resultados = {
        "Total de tomas": round(total_tomas, 1),
        "Total de tabletas": round(total_tabletas, 1),
        "Presentaciones necesarias": presentaciones_necesarias,
        "Fecha de inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Fecha de finalización": fecha_fin.strftime("%Y-%m-%d"),
        "Días este mes": dias_mes_actual,
        "Días próximo mes": dias_mes_siguiente,
        "Tabletas este mes": tabletas_mes_actual,
        "Tabletas próximo mes": tabletas_mes_siguiente
    }

    return resultados
