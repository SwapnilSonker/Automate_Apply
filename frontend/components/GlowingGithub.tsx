import { Github } from 'lucide-react';

export function GlowingGithubIcon() {
  return (
    <div className="relative group">
      <Github className="h-8 w-8 text-gray-900 transition-colors duration-300 group-hover:text-purple-600" />
      <div className="absolute inset-0 rounded-full bg-purple-500/0 group-hover:bg-purple-500/20 blur-xl transition-all duration-300 -z-10" />
    </div>
  );
}