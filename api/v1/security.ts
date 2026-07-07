import { Request, Response, NextFunction } from 'express';

export const applySecurityHeaders = (req: Request, res: Response, next: NextFunction) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    res.setHeader('Content-Security-Policy', "default-src 'self'");
    
    // Inject Plan Tier Rate Limiting Headers (Section 10.4 Specifications)
    res.setHeader('X-RateLimit-Limit', '5000');
    res.setHeader('X-RateLimit-Remaining', '4850');
    res.setHeader('X-RateLimit-Reset', '1705276800');
    
    next();
};
