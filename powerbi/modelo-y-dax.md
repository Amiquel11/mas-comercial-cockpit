# Modelo Power BI y medidas DAX sugeridas

## Modelo recomendado
- Fuente principal: `dbo.vw_powerbi_deal_base`
- Históricos de cambios de etapa: `dbo.fact_deal_stage_event`
- Tablas auxiliares:
  - `Calendario` (tabla fecha)
  - `Metas` (cargada desde Excel en Blob)

Relaciones:
- `Calendario[Date]` -> `vw_powerbi_deal_base[update_time]`
- `Calendario[Date]` -> `fact_deal_stage_event[event_update_time]`
- `Metas[Periodo]` -> `Calendario[YearMonth]`

## DAX sugeridas

### 1) Opps generadas
```DAX
Opps Generadas =
CALCULATE(
    DISTINCTCOUNT(vw_powerbi_deal_base[deal_id]),
    vw_powerbi_deal_base[status] <> "deleted"
)
```

### 2) UF funnel + variación
```DAX
UF Funnel =
SUM(vw_powerbi_deal_base[value])

UF Funnel Variación % =
DIVIDE([UF Funnel] - [UF Funnel Mes Anterior], [UF Funnel Mes Anterior])
```

### 3) Cierres vs meta
```DAX
Cierres =
CALCULATE(
    SUM(vw_powerbi_deal_base[value]),
    vw_powerbi_deal_base[status] = "won"
)

Cierres vs Meta % =
DIVIDE([Cierres], SUM(Metas[MetaCierresUF]))
```

### 4) Forecast mes/trimestre
```DAX
Forecast Mes UF =
CALCULATE(
    SUM(vw_powerbi_deal_base[value]),
    vw_powerbi_deal_base[status] IN {"open", "won"}
)

Forecast Trimestre UF =
CALCULATE([Forecast Mes UF], DATESQTD(Calendario[Date]))
```

### 5) Propuestas enviadas
```DAX
Propuestas Enviadas =
CALCULATE(
    DISTINCTCOUNT(fact_deal_stage_event[deal_id]),
    fact_deal_stage_event[stage_id] = 4
)
```

### 6) Ticket promedio
```DAX
Ticket Promedio =
DIVIDE(
    SUM(vw_powerbi_deal_base[value]),
    DISTINCTCOUNT(vw_powerbi_deal_base[deal_id])
)
```

## Filtros recomendados
Agregar slicers por:
- `BD` (campo de segmentación comercial o unidad de negocio en dim adicional)
- `Cliente` (`org_name`)
- `Ejecutivo` (`user_name`)
- `Etapa` (`stage_name`)
- `Mes/Trimestre` (`Calendario`)
