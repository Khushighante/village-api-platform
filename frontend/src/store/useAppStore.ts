import { create } from 'zustand';
interface AppState {
  userPlan: 'FREE' | 'PREMIUM' | 'PRO' | 'UNLIMITED';
  dailyRequestsUsed: number;
  setPlan: (plan: 'FREE' | 'PREMIUM' | 'PRO' | 'UNLIMITED') => void;
}
export const useAppStore = create<AppState>((set) => ({
  userPlan: 'FREE',
  dailyRequestsUsed: 0,
  setPlan: (plan) => set({ userPlan: plan }),
}));
