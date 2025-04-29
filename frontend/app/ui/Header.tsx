import Link from 'next/link';

const Header = ({ headerState = 'default' }) => {
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

          {/* Conditional Navigation */}
          <nav className="hidden md:flex space-x-8 items-center">
            {/* Show nav items only in 'default' state */}
            {headerState === 'default' && (
              <>
                <a href="#about" className="text-black hover:underline hover:underline-offset-4 transition">
                  About
                </a>
                <a href="#features" className="text-black hover:underline hover:underline-offset-4 transition">
                  Features
                </a>
                <a href="#contact" className="text-black hover:underline hover:underline-offset-4 transition">
                  Contact
                </a>
              </>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-2">
              {/* Empty State: No buttons */}
              {headerState === 'empty' ? null : (
                <>
                  {/* Default State: Show Sign Up and Login buttons */}
                  {headerState === 'default' && (
                    <>
                      <Link href="/signup">
                        <button className="px-4 py-2 bg-gray-300 text-black rounded-full hover:bg-gray-400 transition cursor-pointer">
                          Sign Up
                        </button>
                      </Link>
                      <Link href="/login">
                        <button className="px-4 py-2 bg-gray-300 text-black rounded-full hover:bg-gray-400 transition cursor-pointer">
                          Login
                        </button>
                      </Link>
                    </>
                  )}

                  {/* Logged In State: Show Profile and Logout buttons */}
                  {headerState === 'loggedin' && (
                    <>
                      <Link href="/logout">
                        <button
                          onClick={() => {
                            alert("Logged out");
                          }}
                          className="px-4 py-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition cursor-pointer"
                        >
                          Logout
                        </button>
                      </Link>
                    </>
                  )}
                </>
              )}
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
