import Link from "next/link";

const Footer = () => {

    const currentYear = new Date().getFullYear();
    
    return (
      <footer className="w-full bg-white shadow-inner mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            {/* Branding */}
            <div className="text-black text-lg font-semibold">
              © {currentYear} Kure. All rights reserved.
            </div>
  
            {/* Footer Links */}
            <div className="flex space-x-6">
              <Link href="/privacy" className="text-black hover:underline hover:underline-offset-4 transition">
                Privacy
              </Link>
              <Link href="/terms" className="text-black hover:underline hover:underline-offset-4 transition">
                Terms
              </Link>
            </div>
          </div>
        </div>
      </footer>
    );
  };
  
  export default Footer;
  