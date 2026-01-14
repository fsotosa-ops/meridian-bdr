"""
Templates HTML para emails de Meridian-BDR
Estilo: Enterprise SaaS (Clean & Minimalist with SVG)
"""
from datetime import datetime

def get_daily_summary_html(stats, top_leads, sheet_url, logo_url):
    today = datetime.now().strftime("%d %b, %Y")
    
    # Paleta de colores Enterprise
    brand_color = "#7B3FE4"  # Tu púrpura
    success_bg = "#DCFCE7"
    success_text = "#166534"
    bg_main = "#F3F4F6"
    card_bg = "#FFFFFF"
    text_primary = "#111827"
    text_secondary = "#6B7280"

    # Iconos SVG en línea (Funcionan en Gmail/Outlook)
    icon_chart = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>"""
    icon_check = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#166534" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>"""
    icon_arrow = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ margin: 0; padding: 0; background-color: {bg_main}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: {text_primary}; }}
            .email-wrapper {{ max-width: 600px; margin: 0 auto; padding: 40px 20px; }}
            .card {{ background: {card_bg}; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; border: 1px solid #E5E7EB; }}
            
            /* Header */
            .header {{ padding: 32px; text-align: center; border-bottom: 1px solid #F3F4F6; }}
            .logo {{ width: 48px; height: 48px; border-radius: 8px; margin-bottom: 16px; object-fit: cover; }}
            .title {{ font-size: 24px; font-weight: 700; margin: 0; letter-spacing: -0.5px; }}
            .subtitle {{ color: {text_secondary}; font-size: 14px; margin-top: 8px; font-weight: 500; }}

            /* Stats Grid */
            .stats {{ display: grid; grid-template-columns: 1fr 1fr 1fr; border-bottom: 1px solid #F3F4F6; }}
            .stat-item {{ padding: 24px; text-align: center; border-right: 1px solid #F3F4F6; }}
            .stat-item:last-child {{ border-right: none; }}
            .stat-value {{ font-size: 28px; font-weight: 800; display: block; margin-bottom: 4px; color: {text_primary}; }}
            .stat-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: {text_secondary}; font-weight: 600; }}

            /* Leads List */
            .content {{ padding: 32px; background: #FAFAFA; }}
            .section-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 24px; font-size: 14px; font-weight: 600; color: {text_primary}; text-transform: uppercase; letter-spacing: 0.05em; }}
            
            .lead-card {{ background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; margin-bottom: 16px; transition: all 0.2s; }}
            .lead-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }}
            .lead-name {{ font-size: 16px; font-weight: 700; color: {text_primary}; margin: 0; }}
            .lead-role {{ font-size: 13px; color: {text_secondary}; margin-top: 2px; display: block; }}
            
            .score-pill {{ background: {success_bg}; color: {success_text}; font-size: 13px; font-weight: 700; padding: 4px 10px; border-radius: 100px; display: flex; align-items: center; gap: 4px; }}
            
            .insight-box {{ background: #F9FAFB; border-radius: 8px; padding: 12px; font-size: 13px; line-height: 1.5; color: #4B5563; border: 1px solid #F3F4F6; }}

            /* CTA Button */
            .footer {{ padding: 24px; text-align: center; background: white; border-top: 1px solid #F3F4F6; }}
            .btn {{ background-color: {brand_color}; color: white; text-decoration: none; font-weight: 600; font-size: 14px; padding: 14px 32px; border-radius: 100px; display: inline-block; transition: opacity 0.2s; box-shadow: 0 4px 12px rgba(123, 63, 228, 0.2); }}
            .btn:hover {{ opacity: 0.9; }}
            
            /* Responsive */
            @media (max-width: 600px) {{
                .stats {{ grid-template-columns: 1fr; }}
                .stat-item {{ border-right: none; border-bottom: 1px solid #F3F4F6; padding: 16px; }}
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            <div class="card">
                <div class="header">
                    <img src="{logo_url}" class="logo" alt="Logo">
                    <h1 class="title">Reporte Diario</h1>
                    <p class="subtitle">{today} &bull; Meridian AI Agent</p>
                </div>

                <div class="stats">
                    <div class="stat-item">
                        <span class="stat-value">{stats.get('total', 0)}</span>
                        <span class="stat-label">Extraídos</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value" style="color: #16A34A;">{stats.get('qualified', 0)}</span>
                        <span class="stat-label">Fit Ideal</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value" style="color: #DC2626;">{stats.get('discarded', 0)}</span>
                        <span class="stat-label">Descartados</span>
                    </div>
                </div>

                <div class="content">
                    <div class="section-header">
                        {icon_chart} Top Oportunidades
                    </div>
    """
    
    if top_leads:
        for lead in top_leads[:5]:
            score = lead.get('score', 0)
            html += f"""
                    <div class="lead-card">
                        <div class="lead-header">
                            <div>
                                <h3 class="lead-name">{lead.get('name', 'N/A')}</h3>
                                <span class="lead-role">{lead.get('role', '')} @ {lead.get('company', '')}</span>
                            </div>
                            <div class="score-pill">
                                {score}
                            </div>
                        </div>
                        <div class="insight-box">
                            💡 {lead.get('reason', 'Sin análisis disponible')}
                        </div>
                    </div>
            """
    else:
        html += """<div style="text-align: center; padding: 20px; color: #9CA3AF;">No se encontraron leads calificados hoy.</div>"""

    # Verificamos si hay URL, si no, ponemos un placeholder visual
    href_link = sheet_url if sheet_url else "#"
    
    html += f"""
                </div>
                <div class="footer">
                    <a href="{href_link}" class="btn">
                        Abrir Google Sheets
                    </a>
                    <div style="margin-top: 16px; font-size: 12px; color: #9CA3AF;">
                        Meridian BDR Automation
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html