import Link from 'next/link';

const Header = () => {
  return (
    <header className="w-full bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/">
              <span className="text-2xl font-bold text-black">Kure</span>
            </Link>
          </div>

          {/* Navigation as */}
          <nav className="hidden md:flex space-x-8 items-center">
            <a href="#about" className="text-black hover:underline hover:underline-offset-4 transition">
              About
            </a>
            <a href="#features" className="text-black hover:underline hover:underline-offset-4 transition">
              Features
            </a>
            <a href="#contact" className="text-black hover:underline hover:underline-offset-4 transition">
              Contact
            </a>

            {/* Action Buttons */}
            <Link href="/signup">
              <button className="ml-2 px-2 py-2 bg-white text-black border border-black hover:bg-gray-100 transition">
                Sign Up
              </button>
            </Link>
            <Link href="/login">
              <button className="ml-2 px-2 py-2 bg-white text-black border border-black hover:bg-gray-100 transition">
                Login
              </button>
            </Link>
          </nav>

          {/* Mobile Menu Button (placeholder for later) */}
          <div className="md:hidden">
            {/* Placeholder for mobile menu */}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
