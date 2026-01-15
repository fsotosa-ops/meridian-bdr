"""
Templates HTML para emails de MeridIAn-BDR
Estilo: Sumadots Premium Dark Mode (Tier 1 SaaS)
Paleta: Negro profundo, púrpura neón, verde IA
"""
from datetime import datetime


def get_daily_summary_html(stats, top_leads, sheet_url, logo_url=None):
    """
    Genera el HTML del resumen diario con estilo premium Sumadots.
    
    Args:
        stats: Dict con {total, qualified, discarded}
        top_leads: Lista de leads [{name, role, company, score, reason}]
        sheet_url: URL del Google Sheet
        logo_url: URL del logo (opcional)
    
    Returns:
        String HTML del email
    """
    today = datetime.now().strftime("%d %b, %Y")
    
    # ══════════════════════════════════════════════════════════════
    # PALETA SUMADOTS PREMIUM
    # ══════════════════════════════════════════════════════════════
    colors = {
        'bg_body': '#030303',       # Negro profundo
        'bg_card': '#0A0A0A',       # Card principal
        'bg_elevated': '#111111',   # Elementos elevados
        'bg_input': '#161616',      # Inputs y cards secundarias
        'border': '#1F1F1F',        # Bordes sutiles
        'border_light': '#2A2A2A',  # Bordes más visibles
        
        'text_white': '#FFFFFF',
        'text_primary': '#F5F5F5',
        'text_secondary': '#A1A1A1',
        'text_muted': '#666666',
        
        'brand_purple': '#8B5CF6',  # Púrpura principal
        'brand_purple_light': '#A78BFA',
        'brand_purple_glow': 'rgba(139, 92, 246, 0.15)',
        
        'accent_green': '#10B981',  # Verde IA/éxito
        'accent_green_glow': 'rgba(16, 185, 129, 0.15)',
        
        'score_high': '#10B981',    # Verde - Score alto
        'score_mid': '#F59E0B',     # Amber - Score medio
        'score_low': '#EF4444',     # Rojo - Score bajo
    }
    
    # ══════════════════════════════════════════════════════════════
    # ICONOS SVG PREMIUM
    # ══════════════════════════════════════════════════════════════
    
    # Logo MeridIAn - Globo con nodos de red (estilo IA)
    icon_meridian = f'''
    <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="globeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{colors['brand_purple']};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{colors['accent_green']};stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="22" cy="22" r="20" stroke="url(#globeGradient)" stroke-width="1.5" fill="none"/>
        <ellipse cx="22" cy="22" rx="20" ry="8" stroke="url(#globeGradient)" stroke-width="1" fill="none" opacity="0.6"/>
        <ellipse cx="22" cy="22" rx="8" ry="20" stroke="url(#globeGradient)" stroke-width="1" fill="none" opacity="0.6"/>
        <line x1="2" y1="22" x2="42" y2="22" stroke="url(#globeGradient)" stroke-width="1" opacity="0.4"/>
        <line x1="22" y1="2" x2="22" y2="42" stroke="url(#globeGradient)" stroke-width="1" opacity="0.4"/>
        <circle cx="22" cy="22" r="3" fill="{colors['brand_purple']}"/>
        <circle cx="12" cy="14" r="2" fill="{colors['accent_green']}"/>
        <circle cx="32" cy="14" r="2" fill="{colors['accent_green']}"/>
        <circle cx="12" cy="30" r="2" fill="{colors['accent_green']}"/>
        <circle cx="32" cy="30" r="2" fill="{colors['accent_green']}"/>
        <line x1="22" y1="22" x2="12" y2="14" stroke="{colors['accent_green']}" stroke-width="0.5" opacity="0.5"/>
        <line x1="22" y1="22" x2="32" y2="14" stroke="{colors['accent_green']}" stroke-width="0.5" opacity="0.5"/>
        <line x1="22" y1="22" x2="12" y2="30" stroke="{colors['accent_green']}" stroke-width="0.5" opacity="0.5"/>
        <line x1="22" y1="22" x2="32" y2="30" stroke="{colors['accent_green']}" stroke-width="0.5" opacity="0.5"/>
    </svg>
    '''
    
    # Icono de leads/usuarios
    icon_leads = f'''
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="{colors['text_secondary']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="8.5" cy="7" r="4" stroke="{colors['text_secondary']}" stroke-width="2"/>
        <path d="M20 8V14" stroke="{colors['accent_green']}" stroke-width="2" stroke-linecap="round"/>
        <path d="M23 11H17" stroke="{colors['accent_green']}" stroke-width="2" stroke-linecap="round"/>
    </svg>
    '''
    
    # Icono de check/calificados
    icon_qualified = f'''
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.709 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13631 4.39828 5.49706C5.79935 3.85781 7.69279 2.71537 9.79619 2.24013C11.8996 1.7649 14.1003 1.98232 16.07 2.85999" stroke="{colors['score_high']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M22 4L12 14.01L9 11.01" stroke="{colors['score_high']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    '''
    
    # Icono de descartados
    icon_discarded = f'''
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="{colors['score_low']}" stroke-width="2"/>
        <path d="M15 9L9 15" stroke="{colors['score_low']}" stroke-width="2" stroke-linecap="round"/>
        <path d="M9 9L15 15" stroke="{colors['score_low']}" stroke-width="2" stroke-linecap="round"/>
    </svg>
    '''
    
    # Icono de rayo/insight
    icon_insight = f'''
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill="{colors['brand_purple']}" stroke="{colors['brand_purple']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    '''
    
    # Icono de flecha externa
    icon_external = f'''
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M18 13V19C18 19.5304 17.7893 20.0391 17.4142 20.4142C17.0391 20.7893 16.5304 21 16 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V8C3 7.46957 3.21071 6.96086 3.58579 6.58579C3.96086 6.21071 4.46957 6 5 6H11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M15 3H21V9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    '''

    # ══════════════════════════════════════════════════════════════
    # HTML TEMPLATE
    # ══════════════════════════════════════════════════════════════
    
    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="dark">
        <meta name="supported-color-schemes" content="dark">
        <title>MeridIAn - Resumen Diario</title>
        <style>
            /* Reset & Base */
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                margin: 0;
                padding: 0;
                background-color: {colors['bg_body']};
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                color: {colors['text_primary']};
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }}
            
            /* Container Full Width */
            .email-wrapper {{
                width: 100%;
                max-width: 680px;
                margin: 0 auto;
                background: {colors['bg_card']};
            }}
            
            /* Header con gradiente sutil */
            .header {{
                background: linear-gradient(180deg, {colors['bg_elevated']} 0%, {colors['bg_card']} 100%);
                padding: 40px 32px;
                text-align: center;
                border-bottom: 1px solid {colors['border']};
            }}
            
            .logo-container {{
                margin-bottom: 16px;
            }}
            
            .brand-name {{
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.5px;
                color: {colors['text_white']};
            }}
            
            .brand-name .ia {{
                background: linear-gradient(135deg, {colors['brand_purple']} 0%, {colors['accent_green']} 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .tagline {{
                font-size: 13px;
                color: {colors['text_secondary']};
                margin-top: 4px;
                letter-spacing: 0.5px;
            }}
            
            .date-badge {{
                display: inline-block;
                margin-top: 20px;
                padding: 8px 16px;
                background: {colors['bg_input']};
                border: 1px solid {colors['border']};
                border-radius: 100px;
                font-size: 12px;
                color: {colors['text_secondary']};
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 500;
            }}
            
            /* Stats Section */
            .stats-section {{
                display: table;
                width: 100%;
                border-bottom: 1px solid {colors['border']};
            }}
            
            .stat-item {{
                display: table-cell;
                width: 33.333%;
                padding: 32px 20px;
                text-align: center;
                border-right: 1px solid {colors['border']};
                vertical-align: middle;
            }}
            
            .stat-item:last-child {{
                border-right: none;
            }}
            
            .stat-icon {{
                display: block;
                margin: 0 auto 12px;
            }}
            
            .stat-value {{
                display: block;
                font-size: 36px;
                font-weight: 700;
                letter-spacing: -1px;
                margin-bottom: 6px;
            }}
            
            .stat-value.total {{ color: {colors['text_white']}; }}
            .stat-value.qualified {{ color: {colors['score_high']}; }}
            .stat-value.discarded {{ color: {colors['score_low']}; }}
            
            .stat-label {{
                font-size: 11px;
                color: {colors['text_muted']};
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
            }}
            
            /* Content Section */
            .content {{
                padding: 40px 32px;
            }}
            
            .section-header {{
                display: table;
                width: 100%;
                margin-bottom: 28px;
            }}
            
            .section-title {{
                display: table-cell;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 2px;
                color: {colors['brand_purple']};
            }}
            
            .section-badge {{
                display: table-cell;
                text-align: right;
            }}
            
            .section-badge span {{
                display: inline-block;
                padding: 4px 10px;
                background: {colors['brand_purple_glow']};
                border: 1px solid {colors['brand_purple']};
                border-radius: 4px;
                font-size: 10px;
                color: {colors['brand_purple_light']};
                font-weight: 600;
            }}
            
            /* Lead Cards */
            .lead-card {{
                background: {colors['bg_input']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 16px;
                transition: border-color 0.2s ease;
            }}
            
            .lead-card:hover {{
                border-color: {colors['border_light']};
            }}
            
            .lead-card:last-child {{
                margin-bottom: 0;
            }}
            
            .lead-header {{
                display: table;
                width: 100%;
                margin-bottom: 16px;
            }}
            
            .lead-score-cell {{
                display: table-cell;
                width: 56px;
                vertical-align: top;
            }}
            
            .lead-score {{
                width: 48px;
                height: 48px;
                line-height: 44px;
                text-align: center;
                border-radius: 50%;
                font-size: 16px;
                font-weight: 800;
                border: 2px solid;
                background: {colors['bg_card']};
            }}
            
            .score-high {{
                border-color: {colors['score_high']};
                color: {colors['score_high']};
                box-shadow: 0 0 20px {colors['accent_green_glow']};
            }}
            
            .score-mid {{
                border-color: {colors['score_mid']};
                color: {colors['score_mid']};
            }}
            
            .score-low {{
                border-color: {colors['score_low']};
                color: {colors['score_low']};
            }}
            
            .lead-info {{
                display: table-cell;
                vertical-align: middle;
                padding-left: 16px;
            }}
            
            .lead-name {{
                font-size: 17px;
                font-weight: 700;
                color: {colors['text_white']};
                margin-bottom: 4px;
            }}
            
            .lead-role {{
                font-size: 14px;
                color: {colors['text_secondary']};
            }}
            
            .lead-company {{
                color: {colors['brand_purple_light']};
                font-weight: 500;
            }}
            
            .lead-insight {{
                background: {colors['bg_card']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 14px 16px;
                margin-top: 4px;
            }}
            
            .insight-icon {{
                display: inline-block;
                vertical-align: middle;
                margin-right: 8px;
            }}
            
            .insight-text {{
                font-size: 13px;
                color: {colors['text_secondary']};
                line-height: 1.5;
            }}
            
            /* Empty State */
            .empty-state {{
                text-align: center;
                padding: 48px 32px;
                color: {colors['text_muted']};
            }}
            
            .empty-icon {{
                margin-bottom: 16px;
                opacity: 0.5;
            }}
            
            /* CTA Footer */
            .cta-footer {{
                padding: 40px 32px;
                text-align: center;
                background: linear-gradient(180deg, {colors['bg_card']} 0%, {colors['bg_body']} 100%);
                border-top: 1px solid {colors['border']};
            }}
            
            .cta-button {{
                display: inline-block;
                padding: 16px 48px;
                background: linear-gradient(135deg, {colors['brand_purple']} 0%, #7C3AED 100%);
                color: {colors['text_white']};
                text-decoration: none;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.5px;
                border-radius: 100px;
                box-shadow: 0 4px 24px rgba(139, 92, 246, 0.4);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            
            .cta-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 32px rgba(139, 92, 246, 0.5);
            }}
            
            .cta-icon {{
                display: inline-block;
                vertical-align: middle;
                margin-left: 8px;
            }}
            
            /* Footer Branding */
            .footer-brand {{
                margin-top: 32px;
                padding-top: 24px;
                border-top: 1px solid {colors['border']};
            }}
            
            .footer-text {{
                font-size: 11px;
                color: {colors['text_muted']};
                letter-spacing: 1px;
                text-transform: uppercase;
            }}
            
            .footer-text .highlight {{
                color: {colors['brand_purple']};
            }}
            
            /* Responsive */
            @media only screen and (max-width: 600px) {{
                .header {{ padding: 32px 24px; }}
                .content {{ padding: 32px 24px; }}
                .stat-item {{ padding: 24px 12px; }}
                .stat-value {{ font-size: 28px; }}
                .lead-card {{ padding: 20px; }}
                .cta-footer {{ padding: 32px 24px; }}
                .cta-button {{ padding: 14px 36px; }}
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            
            <!-- Header -->
            <div class="header">
                <div class="logo-container">
                    {icon_meridian}
                </div>
                <div class="brand-name">Merid<span class="ia">IA</span>n</div>
                <div class="tagline">Prospección Inteligente</div>
                <div class="date-badge">{today}</div>
            </div>
            
            <!-- Stats -->
            <div class="stats-section">
                <div class="stat-item">
                    <span class="stat-icon">{icon_leads}</span>
                    <span class="stat-value total">{stats.get('total', 0)}</span>
                    <span class="stat-label">Procesados</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">{icon_qualified}</span>
                    <span class="stat-value qualified">{stats.get('qualified', 0)}</span>
                    <span class="stat-label">Calificados</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">{icon_discarded}</span>
                    <span class="stat-value discarded">{stats.get('discarded', 0)}</span>
                    <span class="stat-label">Descartados</span>
                </div>
            </div>
            
            <!-- Content -->
            <div class="content">
                <div class="section-header">
                    <span class="section-title">Top Oportunidades</span>
                    <span class="section-badge"><span>IA Verified</span></span>
                </div>
    '''
    
    # Generar cards de leads
    if top_leads:
        for lead in top_leads[:5]:
            score = lead.get('score', 0)
            
            # Clase de score
            if score >= 75:
                score_class = 'score-high'
            elif score >= 50:
                score_class = 'score-mid'
            else:
                score_class = 'score-low'
            
            # Limpiar razón
            reason = lead.get('reason', 'Sin información adicional')[:150]
            
            html += f'''
                <div class="lead-card">
                    <div class="lead-header">
                        <div class="lead-score-cell">
                            <div class="lead-score {score_class}">{score}</div>
                        </div>
                        <div class="lead-info">
                            <div class="lead-name">{lead.get('name', 'N/A')}</div>
                            <div class="lead-role">
                                {lead.get('role', 'Sin cargo')} 
                                <span style="color: {colors['text_muted']};">•</span> 
                                <span class="lead-company">{lead.get('company', 'Sin empresa')}</span>
                            </div>
                        </div>
                    </div>
                    <div class="lead-insight">
                        <span class="insight-icon">{icon_insight}</span>
                        <span class="insight-text">{reason}</span>
                    </div>
                </div>
            '''
    else:
        html += f'''
                <div class="empty-state">
                    <div class="empty-icon">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="10" stroke="{colors['text_muted']}" stroke-width="1.5"/>
                            <path d="M8 15C8.5 13.5 10 12 12 12C14 12 15.5 13.5 16 15" stroke="{colors['text_muted']}" stroke-width="1.5" stroke-linecap="round"/>
                            <circle cx="9" cy="9" r="1" fill="{colors['text_muted']}"/>
                            <circle cx="15" cy="9" r="1" fill="{colors['text_muted']}"/>
                        </svg>
                    </div>
                    <div>No se encontraron leads calificados hoy.</div>
                    <div style="margin-top: 8px; font-size: 12px;">Revisa los criterios del ICP en la configuración.</div>
                </div>
        '''
    
    # Footer con CTA
    href_link = sheet_url if sheet_url else "#"
    
    html += f'''
            </div>
            
            <!-- CTA Footer -->
            <div class="cta-footer">
                <a href="{href_link}" class="cta-button" target="_blank">
                    Abrir Dashboard
                    <span class="cta-icon">{icon_external}</span>
                </a>
                
                <div class="footer-brand">
                    <div class="footer-text">
                        Powered by <span class="highlight">Merid<span style="color: {colors['accent_green']};">IA</span>n</span> • Prospección Autónoma
                    </div>
                </div>
            </div>
            
        </div>
    </body>
    </html>
    '''
    
    return html


def get_daily_summary_text(stats, top_leads, sheet_url):
    """
    Versión texto plano del resumen diario.
    Fallback para clientes de email que no soportan HTML.
    """
    today = datetime.now().strftime("%d %b, %Y")
    
    text = f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MeridIAn • Prospección Inteligente
  {today}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 RESUMEN DEL DÍA

  Procesados:    {stats.get('total', 0)}
  Calificados:   {stats.get('qualified', 0)}
  Descartados:   {stats.get('discarded', 0)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 TOP OPORTUNIDADES

'''
    
    if top_leads:
        for i, lead in enumerate(top_leads[:5], 1):
            score = lead.get('score', 0)
            text += f'''
  {i}. {lead.get('name', 'N/A')}
     {lead.get('role', '')} @ {lead.get('company', '')}
     Score: {score}
     → {lead.get('reason', '')[:80]}...

'''
    else:
        text += '''
  No se encontraron leads calificados hoy.
  Revisa los criterios del ICP en la configuración.

'''
    
    text += f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 Ver dashboard completo:
   {sheet_url if sheet_url else 'URL no configurada'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Powered by MeridIAn • Prospección Autónoma
'''
    
    return text