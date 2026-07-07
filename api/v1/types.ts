export interface ApiResponse<T> {
  success: boolean;
  count: number;
  data: T[];
  meta: {
    requestId: string;
    responseTime: number;
    rateLimit: { remaining: number; limit: number; reset: string; };
  };
}
