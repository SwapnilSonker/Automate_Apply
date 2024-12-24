import { Settings } from 'lucide-react';

export function GlowingServicesIcon() {
  return (
    <div className="relative group">
      <Settings className="h-8 w-8 text-gray-900 transition-colors duration-300 group-hover:text-red-600" />
      <div className="absolute inset-0 rounded-full bg-red-500/0 group-hover:bg-red-500/20 blur-xl transition-all duration-300 -z-10" />
    </div>
  );
}