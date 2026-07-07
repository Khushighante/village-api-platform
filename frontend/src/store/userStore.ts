import create from 'zustand';

interface UserState {
  user: any | null;
  isAuthenticated: boolean;
  activePlan: 'Free' | 'Premium' | 'Pro' | 'Unlimited';
  setUser: (user: any) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  isAuthenticated: false,
  activePlan: 'Free',
  setUser: (user) => set({ user, isAuthenticated: !!user, activePlan: user?.plan || 'Free' }),
  logout: () => set({ user: null, isAuthenticated: false, activePlan: 'Free' }),
}));
