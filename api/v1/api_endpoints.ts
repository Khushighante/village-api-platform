import { Request, Response, NextFunction, Router } from 'express';

const router = Router();

// 10.4 Plan Tier Rate Limits Definition Map
const PLAN_TIERS = {
    Free: { daily: 5000, burst: 100 },
    Premium: { daily: 50000, burst: 500 },
    Pro: { daily: 300000, burst: 2000 },
    Unlimited: { daily: 1000000, burst: 5000 }
};

// Simulated Database Fetch Helper for User/Plan Mapping
const getRequestingUserTier = (apiKey: string): 'Free' | 'Premium' | 'Pro' | 'Unlimited' => {
    if (apiKey.includes('premium')) return 'Premium';
    if (apiKey.includes('pro')) return 'Pro';
    return 'Free';
};

// Custom Response Header Injector Wrapper
const sendEnvelope = (res: Response, statusCode: number, data: any, apiKey: string) => {
    const tier = getRequestingUserTier(apiKey);
    const limits = PLAN_TIERS[tier];

    // Inject Security and Rate Limit Headers dynamically (Section 10.3 & 11.1)
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('X-RateLimit-Limit', limits.daily.toString());
    res.setHeader('X-RateLimit-Remaining', (limits.daily - 150).toString()); // Mocked consumption
    res.setHeader('X-RateLimit-Reset', new Date(Date.now() + 3600000).toISOString());

    return res.status(statusCode).json({
        success: true,
        count: Array.isArray(data) ? data.length : 1,
        data: data,
        meta: {
            requestId: `req_${Math.random().toString(36).substring(2, 11)}`,
            responseTime: Math.floor(Math.random() * 35) + 5,
        }
    });
};

// 6.4 GET /search - Village Text Match Array 
router.get('/search', (req: Request, res: Response) => {
    const { q } = req.query;
    const apiKey = String(req.headers['x-api-key'] || '');

    if (!q || String(q).length < 3) {
        return res.status(400).json({
            success: false,
            error: { code: "INVALID_QUERY", message: "Search query too short or invalid (Minimum 3 characters required)." }
        });
    }

    const matchedVillages = [
        { value: "v_525002", label: "Manibeli", fullAddress: "Manibeli, Akkalkuwa, Nandurbar, Maharashtra" }
    ];
    return sendEnvelope(res, 200, matchedVillages, apiKey);
});

// GET /states - Global Territory Lookup
router.get('/states', (req: Request, res: Response) => {
    const apiKey = String(req.headers['x-api-key'] || '');
    const states = [
        { id: "st_27", name: "Maharashtra", code: "MH" },
        { id: "st_07", name: "Delhi", code: "DL" }
    ];
    return sendEnvelope(res, 200, states, apiKey);
});

// GET /states/:id/districts
router.get('/states/:id/districts', (req: Request, res: Response) => {
    const apiKey = String(req.headers['x-api-key'] || '');
    const districts = [{ id: "dist_501", stateId: req.params.id, name: "Nandurbar" }];
    return sendEnvelope(res, 200, districts, apiKey);
});

// GET /districts/:id/subdistricts
router.get('/districts/:id/subdistricts', (req: Request, res: Response) => {
    const apiKey = String(req.headers['x-api-key'] || '');
    const subdistricts = [{ id: "sd_4102", districtId: req.params.id, name: "Akkalkuwa" }];
    return sendEnvelope(res, 200, subdistricts, apiKey);
});

// 6.5 GET /subdistricts/:id/villages (Dropdown Optimized Schema Return)
router.get('/subdistricts/:id/villages', (req: Request, res: Response) => {
    const apiKey = String(req.headers['x-api-key'] || '');
    const dropdownPayload = [
        {
            value: "village_id_525002",
            label: "Manibeli",
            fullAddress: "Manibeli, Akkalkuwa, Nandurbar, Maharashtra, India",
            hierarchy: {
                village: "Manibeli",
                subDistrict: "Akkalkuwa",
                district: "Nandurbar",
                state: "Maharashtra",
                country: "India"
            }
        }
    ];
    return sendEnvelope(res, 200, dropdownPayload, apiKey);
});

export default router;
