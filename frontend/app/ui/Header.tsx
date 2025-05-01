"use client";
import Link from 'next/link';
import { unstable_noStore as noStore } from 'next/cache';
import { useRouter } from "next/navigation";

const Header = ({ headerState = 'default' }) => {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      noStore();
      const host = process.env.NEXT_PUBLIC_ORCHESTRATOR_HOST;
      const port = process.env.NEXT_PUBLIC_ORCHESTRATOR_PORT;
      const orchestratorUrl = `http://${host}:${port}/logout`;

      const response = await fetch(orchestratorUrl, {
        method: 'POST',
        credentials: 'include',
      });

      if (!response.ok) {
        console.error('Logout failed');
        return;
      }

      router.push('/');
    } catch (err) {
      console.error('Error during logout:', err);
    }
  };

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
            <div className="md:flex space-x-8 items-center">
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
                      <Link href={"/notes"} className="text-black hover:underline hover:underline-offset-4 transition">
                        Notes
                      </Link>
                      <Link href={"/dashboard"} className="text-black hover:underline hover:underline-offset-4 transition">
                        Dashboard
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="px-4 py-2 bg-gray-300 text-black rounded-full hover:bg-gray-400 transition cursor-pointer"
                      >
                        Logout
                      </button>
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
