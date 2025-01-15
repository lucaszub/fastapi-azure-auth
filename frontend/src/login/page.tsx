import { LoginForm } from "@/components/login-form"

export default function Page() {
  return (
    <div className="bg-input h-screen w-screen ">
        <nav className="w-full h-20 bg-card fixed ">
            test
        </nav>
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <LoginForm />
      </div>
    </div>
    </div>
  )
}
