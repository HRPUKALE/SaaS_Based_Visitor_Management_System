// To allow importing PNG files, ensure you have a declaration for '*.png' in vite-env.d.ts or a global.d.ts
import React from 'react';
import logo from '../assets/Kanishka Software.png';

const Logo: React.FC<{ className?: string }> = ({ className = '' }) => (
  <img
    src={logo}
    alt="Kanishka Software Logo"
    className={`mx-auto mb-4 max-w-xs w-48 h-auto ${className}`}
    draggable={false}
  />
);

export default Logo; 