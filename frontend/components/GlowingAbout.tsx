import { Info } from 'lucide-react';

export function GlowingAboutIcon() {
  return (
    <div className="relative group">
      <Info className="h-8 w-8 text-gray-900 transition-colors duration-300 group-hover:text-blue-600" />
      <div className="absolute inset-0 rounded-full bg-blue-500/0 group-hover:bg-blue-500/20 blur-xl transition-all duration-300 -z-10" />
    </div>
  );
}