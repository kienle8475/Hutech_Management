import Vue from "vue";
import Router from "vue-router";

// Authen
const Login = () => import("@/views/authen/Login");

// Containers
const TheContainer = () => import("@/containers/TheContainer");

// Application
const Departments = () => import("@/views/departments/Departments");
const Monitoring = () => import("@/views/monitoring/Monitoring");
const Employees = () => import("@/views/employees/Employees");
const Attendances = () => import("@/views/employees/Attendances");
const Students = () => import("@/views/students/Students");
const Students_Checkin = () => import("@/views/recognize/Students_Checkin");
const Recognize = () => import("@/views/recognize/Employee_Recognize");
const ExamSchedule = () => import("@/views/schedules/ExamSchedule");

// Views
const Dashboard = () => import("@/views/Dashboard");

const Colors = () => import("@/views/theme/Colors");
const Typography = () => import("@/views/theme/Typography");

const Charts = () => import("@/views/charts/Charts");
const Widgets = () => import("@/views/widgets/Widgets");

// Views - Components
const Cards = () => import("@/views/base/Cards");
const Forms = () => import("@/views/base/Forms");
const Switches = () => import("@/views/base/Switches");
const Tables = () => import("@/views/base/Tables");
const Tabs = () => import("@/views/base/Tabs");
const Breadcrumbs = () => import("@/views/base/Breadcrumbs");
const Carousels = () => import("@/views/base/Carousels");
const Collapses = () => import("@/views/base/Collapses");
const Jumbotrons = () => import("@/views/base/Jumbotrons");
const ListGroups = () => import("@/views/base/ListGroups");
const Navs = () => import("@/views/base/Navs");
const Navbars = () => import("@/views/base/Navbars");
const Paginations = () => import("@/views/base/Paginations");
const Popovers = () => import("@/views/base/Popovers");
const ProgressBars = () => import("@/views/base/ProgressBars");
const Tooltips = () => import("@/views/base/Tooltips");

// Views - Buttons
const StandardButtons = () => import("@/views/buttons/StandardButtons");
const ButtonGroups = () => import("@/views/buttons/ButtonGroups");
const Dropdowns = () => import("@/views/buttons/Dropdowns");
const BrandButtons = () => import("@/views/buttons/BrandButtons");

// Views - Icons
const CoreUIIcons = () => import("@/views/icons/CoreUIIcons");
const Brands = () => import("@/views/icons/Brands");
const Flags = () => import("@/views/icons/Flags");

// Views - Notifications
const Alerts = () => import("@/views/notifications/Alerts");
const Badges = () => import("@/views/notifications/Badges");
const Modals = () => import("@/views/notifications/Modals");

// Views - Pages
const Page404 = () => import("@/views/pages/Page404");
const Page500 = () => import("@/views/pages/Page500");
//const Login = () => import('@/views/pages/Login')
//const Register = () => import('@/views/pages/Register')

// Users
const Users = () => import("@/views/users/Users");
const User = () => import("@/views/users/User");

Vue.use(Router);

export default new Router({
  mode: "hash", // https://router.vuejs.org/api/#mode
  linkActiveClass: "active",
  scrollBehavior: () => ({ y: 0 }),
  routes: configRoutes(),
});

function configRoutes() {
  return [
    {
      path: "/",
      redirect: "/dashboard",
      name: "Home",
      component: TheContainer,
      children: [
        {
          path: "dashboard",
          name: "Dashboard",
          component: Dashboard,
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "monitoring",
          name: "Monitoring",
          component: Monitoring,
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "departments",
          name: "Departments",
          component: Departments,
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "employees",
          name: "Employees",
          component: Employees,
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "attendances",
          name: "Attendances",
          component: Attendances,
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "students",
          name: "Students",
          component: Students,
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "examschedule",
          name: "Exam Schedule",
          component: ExamSchedule,
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "theme",
          redirect: "/theme/colors",
          name: "Theme",
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "colors",
              name: "Colors",
              component: Colors,
            },
            {
              path: "typography",
              name: "Typography",
              component: Typography,
            },
          ],
        },
        {
          path: "charts",
          name: "Charts",
          component: Charts,
        },
        {
          path: "widgets",
          name: "Widgets",
          component: Widgets,
        },
        {
          path: "users",
          meta: {
            label: "Users",
          },
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "",
              name: "Users",
              component: Users,
              meta: {
                requiresAuth: true,
              },
            },
            {
              path: ":id",
              meta: {
                label: "User Details",
              },
              name: "User",
              component: User,
              meta: {
                requiresAuth: true,
              },
            },
          ],
        },
        {
          path: "base",
          redirect: "/base/cards",
          name: "Base",
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "cards",
              name: "Cards",
              component: Cards,
            },
            {
              path: "forms",
              name: "Forms",
              component: Forms,
            },
            {
              path: "switches",
              name: "Switches",
              component: Switches,
            },
            {
              path: "tables",
              name: "Tables",
              component: Tables,
            },
            {
              path: "tabs",
              name: "Tabs",
              component: Tabs,
            },
            {
              path: "breadcrumbs",
              name: "Breadcrumbs",
              component: Breadcrumbs,
            },
            {
              path: "carousels",
              name: "Carousels",
              component: Carousels,
            },
            {
              path: "collapses",
              name: "Collapses",
              component: Collapses,
            },
            {
              path: "jumbotrons",
              name: "Jumbotrons",
              component: Jumbotrons,
            },
            {
              path: "list-groups",
              name: "List Groups",
              component: ListGroups,
            },
            {
              path: "navs",
              name: "Navs",
              component: Navs,
            },
            {
              path: "navbars",
              name: "Navbars",
              component: Navbars,
            },
            {
              path: "paginations",
              name: "Paginations",
              component: Paginations,
            },
            {
              path: "popovers",
              name: "Popovers",
              component: Popovers,
            },
            {
              path: "progress-bars",
              name: "Progress Bars",
              component: ProgressBars,
            },
            {
              path: "tooltips",
              name: "Tooltips",
              component: Tooltips,
            },
          ],
        },
        {
          path: "buttons",
          redirect: "/buttons/standard-buttons",
          name: "Buttons",
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "standard-buttons",
              name: "Standard Buttons",
              component: StandardButtons,
            },
            {
              path: "button-groups",
              name: "Button Groups",
              component: ButtonGroups,
            },
            {
              path: "dropdowns",
              name: "Dropdowns",
              component: Dropdowns,
            },
            {
              path: "brand-buttons",
              name: "Brand Buttons",
              component: BrandButtons,
            },
          ],
        },
        {
          path: "icons",
          redirect: "/icons/coreui-icons",
          name: "CoreUI Icons",
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "coreui-icons",
              name: "Icons library",
              component: CoreUIIcons,
            },
            {
              path: "brands",
              name: "Brands",
              component: Brands,
            },
            {
              path: "flags",
              name: "Flags",
              component: Flags,
            },
          ],
        },
        {
          path: "notifications",
          redirect: "/notifications/alerts",
          name: "Notifications",
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "alerts",
              name: "Alerts",
              component: Alerts,
            },
            {
              path: "badges",
              name: "Badges",
              component: Badges,
            },
            {
              path: "modals",
              name: "Modals",
              component: Modals,
            },
          ],
        },
      ],
    },
    {
      path: "/auth",
      redirect: "/auth/404",
      name: "auth",
      component: {
        render(c) {
          return c("router-view");
        },
      },
      children: [
        {
          path: "404",
          name: "Page404",
          component: Page404,
        },
        {
          path: "500",
          name: "Page500",
          component: Page500,
        },
        {
          path: "login",
          name: "Login",
          component: Login,
          meta: {
            requiresLogged: true,
          },
        },
        //{
        //  path: 'register',
        //  name: 'Register',
        //  component: Register
        //}
      ],
    },
    {
      path: "/checkin",
      name: "Student Checkin",
      component: Students_Checkin,
    },
    {
      path: "/recognize",
      name: "Recognize",
      component: Recognize,
    },
  ];
}
