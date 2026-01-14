"""
Templates HTML para emails de Meridian-BDR
Estilo: Tarjeta Ejecutiva Compacta (Sumadots Brand)
"""
from datetime import datetime

def get_daily_summary_html(stats, top_leads, sheet_url, logo_url):
    today = datetime.now().strftime("%d %b, %Y")
    primary_color = "#7B3FE4"  # Púrpura vibrante Sumadots
    bg_color = "#F4F5F7"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: {bg_color}; margin: 0; padding: 20px; color: #333; }}
            .card {{ max-width: 500px; margin: 0 auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #E1E4E8; }}
            
            .header {{ background: {primary_color}; padding: 25px; text-align: center; color: white; }}
            .brand-logo {{ background: white; padding: 4px; border-radius: 6px; width: 32px; height: 32px; margin-bottom: 8px; vertical-align: middle; }}
            .header h1 {{ margin: 0; font-size: 20px; font-weight: 600; letter-spacing: -0.5px; }}
            .header p {{ margin: 5px 0 0; font-size: 13px; opacity: 0.9; }}
            
            .stats-row {{ display: flex; border-bottom: 1px solid #EEE; padding: 15px 0; }}
            .stat {{ flex: 1; text-align: center; border-right: 1px solid #EEE; }}
            .stat:last-child {{ border-right: none; }}
            .stat-num {{ font-size: 24px; font-weight: 700; color: #2D3748; display: block; }}
            .stat-label {{ font-size: 10px; text-transform: uppercase; color: #718096; font-weight: 600; letter-spacing: 0.5px; margin-top: 4px; display: block; }}
            
            .list-container {{ padding: 20px; background: #FAFAFA; }}
            .section-label {{ font-size: 11px; font-weight: 700; color: #718096; text-transform: uppercase; margin-bottom: 15px; display: block; }}
            
            .lead-item {{ background: white; padding: 15px; border-radius: 8px; border: 1px solid #EDF2F7; margin-bottom: 12px; display: flex; align-items: flex-start; gap: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }}
            
            .score-badge {{ 
                background: #EDF2F7; color: #2D3748; 
                font-weight: 700; font-size: 13px; 
                padding: 4px 8px; border-radius: 6px; min-width: 24px; text-align: center;
            }}
            .score-high {{ background: #C6F6D5; color: #22543D; }} /* Verde */
            
            .lead-content h3 {{ margin: 0 0 2px; font-size: 14px; font-weight: 600; color: #2D3748; }}
            .lead-meta {{ font-size: 12px; color: #718096; margin-bottom: 6px; display: block; }}
            .lead-insight {{ font-size: 12px; color: #4A5568; line-height: 1.4; background: #F7FAFC; padding: 8px; border-radius: 4px; }}
            
            .btn-container {{ padding: 20px; text-align: center; background: white; border-top: 1px solid #EEE; }}
            .main-btn {{ 
                background: {primary_color}; color: white; 
                text-decoration: none; font-weight: 600; font-size: 14px; 
                padding: 12px 30px; border-radius: 30px; 
                display: inline-block; box-shadow: 0 4px 6px rgba(123, 63, 228, 0.2); 
                transition: transform 0.1s;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <img src="{logo_url}" class="brand-logo">
                <h1>Reporte Diario</h1>
                <p>{today}</p>
            </div>
            
            <div class="stats-row">
                <div class="stat">
                    <span class="stat-num">{stats.get('total', 0)}</span>
                    <span class="stat-label">Total</span>
                </div>
                <div class="stat">
                    <span class="stat-num" style="color: #38A169;">{stats.get('qualified', 0)}</span>
                    <span class="stat-label">Qualified</span>
                </div>
                <div class="stat">
                    <span class="stat-num" style="color: #E53E3E;">{stats.get('discarded', 0)}</span>
                    <span class="stat-label">Discarded</span>
                </div>
            </div>
            
            <div class="list-container">
                <span class="section-label">Top Opportunities</span>
    """
    
    if top_leads:
        for lead in top_leads[:5]:
            score = lead.get('score', 0)
            badge_class = "score-badge score-high" if score >= 80 else "score-badge"
            
            html += f"""
                <div class="lead-item">
                    <div class="{badge_class}">{score}</div>
                    <div class="lead-content">
                        <h3>{lead.get('name', 'N/A')}</h3>
                        <span class="lead-meta">{lead.get('role', '')} @ {lead.get('company', '')}</span>
                        <div class="lead-insight">{lead.get('reason', '')}</div>
                    </div>
                </div>
            """
    else:
        html += "<p style='text-align: center; font-size: 13px; color: #999; padding: 20px;'>No hay leads calificados hoy.</p>"

    html += f"""
            </div>
            <div class="btn-container">
                <a href="{sheet_url}" class="main-btn">Abrir Google Sheets →</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html