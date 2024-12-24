import { Home } from 'lucide-react';

export function GlowingHomeIcon() {
  return (
    <div className="relative group">
      <Home className="h-8 w-8 text-gray-900 transition-colors duration-300 group-hover:text-yellow-600" />
      <div className="absolute inset-0 rounded-full bg-yellow-500/0 group-hover:bg-yellow-500/20 blur-xl transition-all duration-300 -z-10" />
    </div>
  );
}