import Link from 'next/link';
import React from 'react';

const Header = () => {
    return (

        <div>
        <nav>
          <ul className="flex  justify-evenly ">
            <li>
              <Link href="#home" 
              className="text-white hover:bg-white/20 hover:text-blue-700 px-4 py-2 rounded-lg transition duration-300 ease-in-out">
                Home
              </Link>
            </li>
            <li>
              <Link href="#about" className="text-white hover:bg-white/20 hover:text-blue-700 px-4 py-2 rounded-lg transition duration-300 ease-in-out">
                About
              </Link>
            </li>
            <li>
              <Link href="#services" className="text-white hover:bg-white/20 hover:text-blue-700 px-4 py-2 rounded-lg transition duration-300 ease-in-out">
                Services
              </Link>
            </li>
            <li>
              <Link href="#contact" className="text-white hover:bg-white/20 hover:text-blue-700 px-4 py-2 rounded-lg transition duration-300 ease-in-out">
                Contact
              </Link>
            </li>
          </ul>
        </nav>
        </div>

    );
};

export default Header;
