import MainLayout from "./layout/MainLayout.jsx";
import AppRouter from "./router.jsx";

export default function App() {
  return (
    <MainLayout>
      <AppRouter />
    </MainLayout>
  );
}