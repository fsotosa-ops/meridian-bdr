"""
Notificaciones por email para Meridian-BDR
Envía resumen diario al BDR
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class EmailNotifier:
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")  # App password para Gmail
        self.bdr_email = os.getenv("BDR_EMAIL")
        self.sheet_url = os.getenv("GOOGLE_SHEET_URL", "")
        
        self.enabled = all([self.sender_email, self.sender_password, self.bdr_email])
        
        if not self.enabled:
            print("⚠️ Email no configurado. Agrega SENDER_EMAIL, SENDER_PASSWORD y BDR_EMAIL al .env")
    
    def send_daily_summary(self, stats, top_leads):
        """
        Envía resumen diario al BDR.
        
        Args:
            stats: Dict con estadísticas {total, qualified, discarded}
            top_leads: Lista de dicts con top leads [{name, company, role, score, reason}]
        """
        
        if not self.enabled:
            print("📧 Email deshabilitado - saltando notificación")
            return False
        
        today = datetime.now().strftime("%d de %B, %Y")
        
        # Construir HTML del email
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-box {{ background: white; padding: 15px 25px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .stat-number {{ font-size: 28px; font-weight: bold; color: #667eea; }}
                .stat-label {{ font-size: 12px; color: #666; }}
                .lead-card {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .lead-name {{ font-weight: bold; font-size: 16px; }}
                .lead-company {{ color: #666; }}
                .lead-score {{ background: #667eea; color: white; padding: 3px 10px; border-radius: 15px; font-size: 12px; }}
                .lead-reason {{ font-size: 13px; color: #555; margin-top: 8px; }}
                .cta-button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 15px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Meridian-BDR</h1>
                <p>Resumen Diario - {today}</p>
            </div>
            
            <div class="content">
                <h2>📊 Resumen</h2>
                
                <table width="100%" cellpadding="10">
                    <tr>
                        <td align="center" style="background: white; border-radius: 8px;">
                            <div style="font-size: 28px; font-weight: bold; color: #667eea;">{stats.get('total', 0)}</div>
                            <div style="font-size: 12px; color: #666;">Leads extraídos</div>
                        </td>
                        <td align="center" style="background: white; border-radius: 8px;">
                            <div style="font-size: 28px; font-weight: bold; color: #27ae60;">{stats.get('qualified', 0)}</div>
                            <div style="font-size: 12px; color: #666;">Calificados (≥70)</div>
                        </td>
                        <td align="center" style="background: white; border-radius: 8px;">
                            <div style="font-size: 28px; font-weight: bold; color: #e74c3c;">{stats.get('discarded', 0)}</div>
                            <div style="font-size: 12px; color: #666;">Descartados</div>
                        </td>
                    </tr>
                </table>
                
                <h2 style="margin-top: 30px;">🏆 Top Leads para Revisar</h2>
        """
        
        if top_leads:
            for i, lead in enumerate(top_leads[:5], 1):
                html += f"""
                <div class="lead-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="lead-name">{i}. {lead.get('name', 'N/A')}</span>
                            <span class="lead-score">Score: {lead.get('score', 0)}</span>
                        </div>
                    </div>
                    <div class="lead-company">{lead.get('role', '')} @ {lead.get('company', '')}</div>
                    <div class="lead-reason">💡 {lead.get('reason', '')[:100]}...</div>
                </div>
                """
        else:
            html += """
                <p style="text-align: center; color: #666;">No hay leads calificados hoy. Revisa los criterios del ICP.</p>
            """
        
        html += f"""
                <div style="text-align: center;">
                    <a href="{self.sheet_url}" class="cta-button">👉 Ver todos los leads en Google Sheets</a>
                </div>
            </div>
            
            <div class="footer">
                <p>Meridian-BDR - Tu agente de prospección automatizado</p>
                <p>El BDR duerme, Meridian trabaja 🚀</p>
            </div>
        </body>
        </html>
        """
        
        # Versión texto plano
        text = f"""
🎯 MERIDIAN-BDR - Resumen Diario
{today}

📊 RESUMEN:
• Leads extraídos: {stats.get('total', 0)}
• Leads calificados (Score ≥70): {stats.get('qualified', 0)}
• Descartados: {stats.get('discarded', 0)}

🏆 TOP LEADS PARA REVISAR:
"""
        for i, lead in enumerate(top_leads[:5], 1):
            text += f"""
{i}. {lead.get('name', 'N/A')} - {lead.get('role', '')} @ {lead.get('company', '')}
   Score: {lead.get('score', 0)} | {lead.get('reason', '')[:80]}...
"""
        
        text += f"""
👉 Ver todos los leads: {self.sheet_url}
        """
        
        # Enviar email
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"🎯 Meridian-BDR: {stats.get('qualified', 0)} leads calificados - {today}"
            msg["From"] = self.sender_email
            msg["To"] = self.bdr_email
            
            msg.attach(MIMEText(text, "plain"))
            msg.attach(MIMEText(html, "html"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.bdr_email, msg.as_string())
            
            print(f"📧 Email enviado a {self.bdr_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            return False


def test_email():
    """Test de envío de email"""
    notifier = EmailNotifier()
    
    stats = {"total": 23, "qualified": 5, "discarded": 18}
    top_leads = [
        {"name": "Juan Pérez", "role": "Dir. Compras", "company": "Química MX", "score": 92, "reason": "Importa $15M USD en químicos industriales"},
        {"name": "María González", "role": "Supply Chain Manager", "company": "Aceros Norte", "score": 85, "reason": "Importa $8M USD en acero de China"},
        {"name": "Carlos Ruiz", "role": "Gerente Comercial", "company": "Plásticos SA", "score": 78, "reason": "Importa polímeros y resinas"},
    ]
    
    notifier.send_daily_summary(stats, top_leads)


if __name__ == "__main__":
    test_email()
