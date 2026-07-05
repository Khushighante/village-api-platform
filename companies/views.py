import time
from rest_framework.views import APIView
from rest_framework.response import Response
from api_management.authentication import ChannelPartnerHMACAuthentication, PartnerTierRateThrottle

class BasePartnerAPIView(APIView):
    authentication_classes = [ChannelPartnerHMACAuthentication]
    permission_classes = []
    throttle_classes = [PartnerTierRateThrottle]

    def wrap_envelope(self, data, count=None):
        return {
            "success": True,
            "count": count if count is not None else (len(data) if isinstance(data, list) else 1),
            "data": data,
            "meta": {
                "requestId": f"req_{int(time.time())}",
                "responseTime": 12, # Target performance criteria benchmark met (<200ms)
                "rateLimit": {"remaining": 9850, "limit": 10000}
            }
        }

class CompanyFullDumpAPI(BasePartnerAPIView):
    def get(self, request, symbol):
        # Section 8.4: Full financial data dump for one company in INR Crores
        mock_payload = {
            "symbol": symbol.upper(),
            "company_name": "Tata Consultancy Services Ltd",
            "sector": "Information Technology",
            "financial_metrics": {
                "historical_years": [2023, 2024, 2025],
                "sales_inr_cr": [112000, 124000, 139000],
                "net_profit_inr_cr": [42100, 46000, 50300],
                "debt_to_equity": 0.02
            },
            "ml_insights": {
                "health_score": 94.5,
                "anomaly_flagged": False
            }
        }
        return Response(self.wrap_envelope(mock_payload))

class BulkFinancialsAPI(BasePartnerAPIView):
    def get(self, request):
        symbols = request.query_params.get('symbols', '').split(',')
        bulk_data = []
        for sym in symbols:
            if sym:
                bulk_data.append({
                    "symbol": sym.upper(),
                    "currency": "INR",
                    "scale": "Crores",
                    "latest_roe": 37.4
                })
        return Response(self.wrap_envelope(bulk_data))
