from argparse import Namespace

from fletx.cli.commands.base import (
    FletPassthroughCommand, CommandParser
)


def _flag(val, name):
    """Return [name] if val is truthy, else []."""
    return [name] if val else []


def _opt(val, name):
    """Return [name, str(val)] if val is not None and not the default, else []."""
    return [name, str(val)] if val is not None else []


def _opt_skip_default(val, name, default):
    """Return [name, str(val)] if val != default, else []."""
    return [name, str(val)] if val != default else []


def _multi(val, name):
    """Return [name, *vals] if val is not None, else []."""
    return [name, *val] if val else []


def _add_build_config_args(parser: CommandParser, include_both_positional=True):
    """Add the common build configuration arguments shared by build and debug."""

    if include_both_positional:
        parser.add_argument(
            "platform", nargs="?",
            help="Target platform (macos, linux, windows, web, apk, aab, ipa, ios-simulator)"
        )
        parser.add_argument(
            "python_app_path", nargs="?", default=".",
            help="Path to a Python program directory (default: .)"
        )

    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Enable verbose output. Use -v for standard, -vv for detailed")

    g1 = parser.add_argument_group("build output")
    g1.add_argument("-o", "--output", dest="output_dir",
                    help="Output directory for the final executable/bundle")

    g2 = parser.add_argument_group("platform")
    g2.add_argument("--arch", nargs="*",
                    help="Build for specific CPU architectures (macOS and Android only)")
    g2.add_argument("--exclude", nargs="*",
                    help="Files/directories to exclude from the package")

    g3 = parser.add_argument_group("caching")
    g3.add_argument("--clear-cache", action="store_true",
                    help="Remove any existing build cache before starting")

    g4 = parser.add_argument_group("application metadata")
    g4.add_argument("--project", help="Project name for bundle IDs and identifiers")
    g4.add_argument("--artifact", help="Executable or bundle name on disk")
    g4.add_argument("--description", help="Short description of the application")
    g4.add_argument("--product", help="Display name shown in app launchers")
    g4.add_argument("--org", help="Organization name in reverse domain notation")
    g4.add_argument("--bundle-id", help="Bundle ID for the application")
    g4.add_argument("--company", help="Company name to display in about dialogs")
    g4.add_argument("--copyright", help="Copyright text for about dialogs")
    g4.add_argument("--build-number", help="Internal version number identifier")
    g4.add_argument("--build-version", help="Version string x.y.z shown to users")
    g4.add_argument("--module-name", help="Python module name with the app entry point")

    g5 = parser.add_argument_group("splash screen")
    g5.add_argument("--splash-color", help="Background color of splash screen")
    g5.add_argument("--splash-dark-color", help="Dark mode splash background color")
    g5.add_argument("--no-web-splash", action="store_true",
                    help="Disable splash screen on web")
    g5.add_argument("--no-ios-splash", action="store_true",
                    help="Disable splash screen on iOS")
    g5.add_argument("--no-android-splash", action="store_true",
                    help="Disable splash screen on Android")

    g6 = parser.add_argument_group("iOS signing")
    g6.add_argument("--ios-team-id", help="Apple developer team ID")
    g6.add_argument("--ios-export-method", help="Export method for iOS app bundle")
    g6.add_argument("--ios-provisioning-profile",
                    help="Provisioning profile name or UUID")
    g6.add_argument("--ios-signing-certificate",
                    help="Signing certificate name or SHA-1 hash")

    g7 = parser.add_argument_group("web")
    g7.add_argument("--base-url", help="Base URL from which the app is served")
    g7.add_argument("--web-renderer", choices=["auto", "canvaskit", "skwasm"],
                    help="Flutter web renderer")
    g7.add_argument("--route-url-strategy", choices=["path", "hash"],
                    help="URL strategy for routing")
    g7.add_argument("--pwa-background-color",
                    help="Initial background color for the web app")
    g7.add_argument("--pwa-theme-color",
                    help="Default color for the web app UI")
    g7.add_argument("--no-wasm", action="store_true",
                    help="Disable WASM target for web build")
    g7.add_argument("--no-cdn", action="store_true",
                    help="Disable CDN loading for CanvasKit, Pyodide, fonts")

    g8 = parser.add_argument_group("Android")
    g8.add_argument("--android-adaptive-icon-background",
                    help="Background color for Android adaptive icons")
    g8.add_argument("--split-per-abi", action="store_true",
                    help="Split APKs per ABIs")
    g8.add_argument("--android-signing-key-store",
                    help="Path to Android upload keystore .jks file")
    g8.add_argument("--android-signing-key-store-password",
                    help="Android signing store password")
    g8.add_argument("--android-signing-key-password",
                    help="Android signing key password")
    g8.add_argument("--android-signing-key-alias",
                    help="Android signing key alias")
    g8.add_argument("--android-features", nargs="*",
                    help="Key=value features for AndroidManifest.xml")
    g8.add_argument("--android-permissions", nargs="*",
                    help="Key=value permissions for AndroidManifest.xml")
    g8.add_argument("--android-meta-data", nargs="*",
                    help="Key=value meta-data for AndroidManifest.xml")
    g8.add_argument("--deep-linking-scheme",
                    help="Deep linking URL scheme for iOS and Android")
    g8.add_argument("--deep-linking-host",
                    help="Deep linking URL host for iOS and Android")

    g9 = parser.add_argument_group("permissions")
    g9.add_argument("--permissions", nargs="*",
                    choices=["location", "camera", "microphone", "photo_library"],
                    help="Pre-defined cross-platform permissions")

    g10 = parser.add_argument_group("optimization")
    g10.add_argument("--compile-app", action="store_true",
                     help="Pre-compile app .py files to .pyc")
    g10.add_argument("--compile-packages", action="store_true",
                     help="Pre-compile site-packages .py files to .pyc")
    g10.add_argument("--cleanup-app", action="store_true",
                     help="Remove unnecessary app files upon packaging")
    g10.add_argument("--cleanup-app-files", nargs="*",
                     help="Globs to delete extra app files and directories")
    g10.add_argument("--cleanup-packages", action="store_true",
                     help="Remove unnecessary package files upon packaging")
    g10.add_argument("--cleanup-package-files", nargs="*",
                     help="Globs to delete extra package files and directories")

    g11 = parser.add_argument_group("advanced")
    g11.add_argument("--flutter-build-args", nargs="*",
                     help="Additional arguments for flutter build command")
    g11.add_argument("--source-packages", nargs="*",
                     help="Python packages to install from source distributions")
    g11.add_argument("--info-plist", nargs="*",
                     help="Key=value pairs to add to Info.plist")
    g11.add_argument("--macos-entitlements", nargs="*",
                     help="Key=value entitlements for macOS")
    g11.add_argument("--template",
                     help="Directory or git URL with Flutter bootstrap template")
    g11.add_argument("--template-dir",
                     help="Relative path to template in a repository")
    g11.add_argument("--template-ref",
                     help="Branch, tag or commit ID for the template")

    g12 = parser.add_argument_group("utility")
    g12.add_argument("--show-platform-matrix", action="store_true",
                     help="Display build platform matrix table then exit")
    g12.add_argument("--no-rich-output", action="store_true",
                     help="Disable rich output, prefer plain text")
    g12.add_argument("--yes", action="store_true",
                     help="Answer yes to all prompts")
    g12.add_argument("--skip-flutter-doctor", action="store_true",
                     help="Skip running Flutter doctor")


def _build_config_flet_args(args: Namespace) -> list[str]:
    """Convert the common build config Namespace to flet CLI arguments."""
    result = []
    result.extend(_opt(args.output_dir, "-o"))
    result.extend(_multi(args.arch, "--arch"))
    result.extend(_multi(args.exclude, "--exclude"))
    result.extend(_flag(args.clear_cache, "--clear-cache"))
    result.extend(_opt(args.project, "--project"))
    result.extend(_opt(args.artifact, "--artifact"))
    result.extend(_opt(args.description, "--description"))
    result.extend(_opt(args.product, "--product"))
    result.extend(_opt(args.org, "--org"))
    result.extend(_opt(args.bundle_id, "--bundle-id"))
    result.extend(_opt(args.company, "--company"))
    result.extend(_opt(args.copyright, "--copyright"))
    result.extend(_opt(args.build_number, "--build-number"))
    result.extend(_opt(args.build_version, "--build-version"))
    result.extend(_opt(args.module_name, "--module-name"))
    result.extend(_opt(args.splash_color, "--splash-color"))
    result.extend(_opt(args.splash_dark_color, "--splash-dark-color"))
    result.extend(_flag(args.no_web_splash, "--no-web-splash"))
    result.extend(_flag(args.no_ios_splash, "--no-ios-splash"))
    result.extend(_flag(args.no_android_splash, "--no-android-splash"))
    result.extend(_opt(args.ios_team_id, "--ios-team-id"))
    result.extend(_opt(args.ios_export_method, "--ios-export-method"))
    result.extend(_opt(args.ios_provisioning_profile, "--ios-provisioning-profile"))
    result.extend(_opt(args.ios_signing_certificate, "--ios-signing-certificate"))
    result.extend(_opt(args.base_url, "--base-url"))
    result.extend(_opt(args.web_renderer, "--web-renderer"))
    result.extend(_opt(args.route_url_strategy, "--route-url-strategy"))
    result.extend(_opt(args.pwa_background_color, "--pwa-background-color"))
    result.extend(_opt(args.pwa_theme_color, "--pwa-theme-color"))
    result.extend(_flag(args.no_wasm, "--no-wasm"))
    result.extend(_flag(args.no_cdn, "--no-cdn"))
    result.extend(_opt(args.android_adaptive_icon_background, "--android-adaptive-icon-background"))
    result.extend(_flag(args.split_per_abi, "--split-per-abi"))
    result.extend(_opt(args.android_signing_key_store, "--android-signing-key-store"))
    result.extend(_opt(args.android_signing_key_store_password, "--android-signing-key-store-password"))
    result.extend(_opt(args.android_signing_key_password, "--android-signing-key-password"))
    result.extend(_opt(args.android_signing_key_alias, "--android-signing-key-alias"))
    result.extend(_multi(args.android_features, "--android-features"))
    result.extend(_multi(args.android_permissions, "--android-permissions"))
    result.extend(_multi(args.android_meta_data, "--android-meta-data"))
    result.extend(_opt(args.deep_linking_scheme, "--deep-linking-scheme"))
    result.extend(_opt(args.deep_linking_host, "--deep-linking-host"))
    result.extend(_multi(args.permissions, "--permissions"))
    result.extend(_flag(args.compile_app, "--compile-app"))
    result.extend(_flag(args.compile_packages, "--compile-packages"))
    result.extend(_flag(args.cleanup_app, "--cleanup-app"))
    result.extend(_multi(args.cleanup_app_files, "--cleanup-app-files"))
    result.extend(_flag(args.cleanup_packages, "--cleanup-packages"))
    result.extend(_multi(args.cleanup_package_files, "--cleanup-package-files"))
    result.extend(_multi(args.flutter_build_args, "--flutter-build-args"))
    result.extend(_multi(args.source_packages, "--source-packages"))
    result.extend(_multi(args.info_plist, "--info-plist"))
    result.extend(_multi(args.macos_entitlements, "--macos-entitlements"))
    result.extend(_opt(args.template, "--template"))
    result.extend(_opt(args.template_dir, "--template-dir"))
    result.extend(_opt(args.template_ref, "--template-ref"))
    result.extend(_flag(args.show_platform_matrix, "--show-platform-matrix"))
    result.extend(_flag(args.no_rich_output, "--no-rich-output"))
    result.extend(_flag(args.yes, "--yes"))
    result.extend(_flag(args.skip_flutter_doctor, "--skip-flutter-doctor"))
    return result


class BuildCommand(FletPassthroughCommand):
    """Build a Flet app into a platform-specific executable or bundle."""

    command_name = "build"
    flet_subcommand = "build"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "platform", nargs="?",
            choices=["macos", "linux", "windows", "web", "apk", "aab", "ipa", "ios-simulator"],
            help="Target platform or package type"
        )
        parser.add_argument(
            "python_app_path", nargs="?", default=".",
            help="Path to a Python program directory (default: .)"
        )
        _add_build_config_args(parser, include_both_positional=False)

    def _build_flet_args(self, args: Namespace) -> list[str]:
        result = []
        if args.platform:
            result.append(args.platform)
        if args.python_app_path and args.python_app_path != ".":
            result.append(args.python_app_path)
        result.extend(_build_config_flet_args(args))
        return result


class DebugCommand(FletPassthroughCommand):
    """Run a Flet app in debug mode on a specified platform."""

    command_name = "debug"
    flet_subcommand = "debug"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "platform", nargs="?",
            choices=["macos", "linux", "windows", "web", "ios", "android"],
            help="Target platform to run the app on"
        )
        parser.add_argument(
            "python_app_path", nargs="?", default=".",
            help="Path to a Python program directory (default: .)"
        )

        dg = parser.add_argument_group("debug options")
        dg.add_argument("--device-id", "-d",
                        help="Device ID to run the app on for iOS and Android")
        dg.add_argument("--show-devices", action="store_true",
                        help="Show connected devices for iOS and Android")
        dg.add_argument("--release", action="store_true",
                        help="Build the app in release mode")
        dg.add_argument("--route",
                        help="Route to open the app on for web, iOS and Android")

        _add_build_config_args(parser, include_both_positional=False)

    def _build_flet_args(self, args: Namespace) -> list[str]:
        result = []
        if args.platform:
            result.append(args.platform)
        if args.python_app_path and args.python_app_path != ".":
            result.append(args.python_app_path)
        result.extend(_opt(args.device_id, "--device-id"))
        result.extend(_flag(args.show_devices, "--show-devices"))
        result.extend(_flag(args.release, "--release"))
        result.extend(_opt(args.route, "--route"))
        result.extend(_build_config_flet_args(args))
        return result


class PackCommand(FletPassthroughCommand):
    """Package a Flet app into a standalone executable using PyInstaller."""

    command_name = "pack"
    flet_subcommand = "pack"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("script",
                            help="Path to the Python script that launches the app")
        parser.add_argument("-i", "--icon",
                            help="Path to an icon file (.ico, .png, .icns)")
        parser.add_argument("-n", "--name",
                            help="Name for the generated executable or app bundle")
        parser.add_argument("-D", "--onedir", action="store_true",
                            help="Create a one-folder bundle (Windows only)")
        parser.add_argument("--distpath",
                            help="Output directory (default: dist)")
        parser.add_argument("--add-data", nargs="*",
                            help="Non-binary files in source:destination format")
        parser.add_argument("--add-binary", nargs="*",
                            help="Binary files in source:destination[:platform] format")
        parser.add_argument("--hidden-import", nargs="*",
                            help="Python modules not detected by static analysis")
        parser.add_argument("--product-name",
                            help="Product name embedded in the executable")
        parser.add_argument("--file-description",
                            help="File description embedded in the executable (Windows)")
        parser.add_argument("--product-version",
                            help="Product version string")
        parser.add_argument("--file-version",
                            help="File version in n.n.n.n format (Windows)")
        parser.add_argument("--company-name",
                            help="Company name metadata (Windows)")
        parser.add_argument("--copyright",
                            help="Copyright string embedded in the executable")
        parser.add_argument("--codesign-identity",
                            help="Code signing identity (macOS)")
        parser.add_argument("--bundle-id",
                            help="Bundle identifier for macOS packaging")
        parser.add_argument("--debug-console",
                            help="Show Python debug console window")
        parser.add_argument("--uac-admin", action="store_true",
                            help="Request admin permissions on start (Windows)")
        parser.add_argument("--pyinstaller-build-args", nargs="*",
                            help="Additional raw PyInstaller arguments")
        parser.add_argument("-y", "--yes", action="store_true",
                            help="Non-interactive mode, skip all prompts")

    def _build_flet_args(self, args: Namespace) -> list[str]:
        result = [args.script]
        result.extend(_opt(args.icon, "-i"))
        result.extend(_opt(args.name, "-n"))
        result.extend(_flag(args.onedir, "-D"))
        result.extend(_opt(args.distpath, "--distpath"))
        result.extend(_multi(args.add_data, "--add-data"))
        result.extend(_multi(args.add_binary, "--add-binary"))
        result.extend(_multi(args.hidden_import, "--hidden-import"))
        result.extend(_opt(args.product_name, "--product-name"))
        result.extend(_opt(args.file_description, "--file-description"))
        result.extend(_opt(args.product_version, "--product-version"))
        result.extend(_opt(args.file_version, "--file-version"))
        result.extend(_opt(args.company_name, "--company-name"))
        result.extend(_opt(args.copyright, "--copyright"))
        result.extend(_opt(args.codesign_identity, "--codesign-identity"))
        result.extend(_opt(args.bundle_id, "--bundle-id"))
        result.extend(_opt(args.debug_console, "--debug-console"))
        result.extend(_flag(args.uac_admin, "--uac-admin"))
        result.extend(_multi(args.pyinstaller_build_args, "--pyinstaller-build-args"))
        result.extend(_flag(args.yes, "-y"))
        return result


class PublishCommand(FletPassthroughCommand):
    """Compile and publish a Flet app as a static web application."""

    command_name = "publish"
    flet_subcommand = "publish"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("script", nargs="?", default=".",
                            help="Path to the Python script (default: .)")
        parser.add_argument("--pre", action="store_true",
                            help="Allow pre-release Python packages via micropip")
        parser.add_argument("-a", "--assets", dest="assets_dir",
                            help="Path to a directory with static assets")
        parser.add_argument("--distpath",
                            help="Output directory (default: dist)")
        parser.add_argument("--app-name",
                            help="Full name of the application (PWA metadata)")
        parser.add_argument("--app-short-name",
                            help="Short version of the application name")
        parser.add_argument("--app-description",
                            help="Short description of the application")
        parser.add_argument("--base-url",
                            help="Base URL path for subdirectory hosting")
        parser.add_argument("--web-renderer", choices=["auto", "canvaskit", "skwasm"],
                            default="auto",
                            help="Flutter web renderer")
        parser.add_argument("--route-url-strategy", choices=["path", "hash"],
                            default="path",
                            help="URL strategy for routing")
        parser.add_argument("--pwa-background-color",
                            help="Initial background color for the web app")
        parser.add_argument("--pwa-theme-color",
                            help="Default color of the browser UI")
        parser.add_argument("--no-cdn", action="store_true",
                            help="Disable CDN loading for offline deployments")

    def _build_flet_args(self, args: Namespace) -> list[str]:
        result = []
        if args.script and args.script != ".":
            result.append(args.script)
        result.extend(_flag(args.pre, "--pre"))
        result.extend(_opt(args.assets_dir, "-a"))
        result.extend(_opt(args.distpath, "--distpath"))
        result.extend(_opt(args.app_name, "--app-name"))
        result.extend(_opt(args.app_short_name, "--app-short-name"))
        result.extend(_opt(args.app_description, "--app-description"))
        result.extend(_opt(args.base_url, "--base-url"))
        result.extend(_opt_skip_default(args.web_renderer, "--web-renderer", "auto"))
        result.extend(_opt_skip_default(args.route_url_strategy, "--route-url-strategy", "path"))
        result.extend(_opt(args.pwa_background_color, "--pwa-background-color"))
        result.extend(_opt(args.pwa_theme_color, "--pwa-theme-color"))
        result.extend(_flag(args.no_cdn, "--no-cdn"))
        return result


class ServeCommand(FletPassthroughCommand):
    """Serve static files with a lightweight web server."""

    command_name = "serve"
    flet_subcommand = "serve"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("web_root", nargs="?", default="./build/web",
                            help="Directory to serve (default: ./build/web)")
        parser.add_argument("-p", "--port", type=int,
                            help="Port number to serve on (default: 8000)")

    def _build_flet_args(self, args: Namespace) -> list[str]:
        result = []
        if args.web_root and args.web_root != "./build/web":
            result.append(args.web_root)
        result.extend(_opt(args.port, "-p"))
        return result


class EmulatorsCommand(FletPassthroughCommand):
    """List, create, and launch emulators."""

    command_name = "emulators"
    flet_subcommand = "emulators"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "action", nargs="?", choices=["start", "create", "delete"],
            help="Action to perform"
        )
        parser.add_argument("emulator", nargs="?",
                            help="Emulator ID or name")
        parser.add_argument("--cold", action="store_true",
                            help="Cold boot the emulator")
        parser.add_argument("--no-rich-output", action="store_true",
                            help="Disable rich output")
        parser.add_argument("--yes", action="store_true",
                            help="Answer yes to all prompts")
        parser.add_argument("--skip-flutter-doctor", action="store_true",
                            help="Skip Flutter doctor")

    def _build_flet_args(self, args: Namespace) -> list[str]:
        result = []
        if args.action:
            result.append(args.action)
        if args.emulator:
            result.append(args.emulator)
        result.extend(_flag(args.cold, "--cold"))
        result.extend(_flag(args.no_rich_output, "--no-rich-output"))
        result.extend(_flag(args.yes, "--yes"))
        result.extend(_flag(args.skip_flutter_doctor, "--skip-flutter-doctor"))
        return result


class DevicesCommand(FletPassthroughCommand):
    """List connected iOS and Android devices."""

    command_name = "devices"
    flet_subcommand = "devices"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "platform", nargs="?", choices=["ios", "android"],
            help="Target platform to list devices for"
        )
        parser.add_argument("--device-timeout", type=int,
                            help="Time in seconds to wait for devices (default: 10)")
        parser.add_argument("--device-connection",
                            choices=["both", "attached", "wireless"],
                            help="Filter by connection type")
        parser.add_argument("--no-rich-output", action="store_true",
                            help="Disable rich output")
        parser.add_argument("--yes", action="store_true",
                            help="Answer yes to all prompts")
        parser.add_argument("--skip-flutter-doctor", action="store_true",
                            help="Skip Flutter doctor")

    def _build_flet_args(self, args: Namespace) -> list[str]:
        result = []
        if args.platform:
            result.append(args.platform)
        result.extend(_opt(args.device_timeout, "--device-timeout"))
        result.extend(_opt(args.device_connection, "--device-connection"))
        result.extend(_flag(args.no_rich_output, "--no-rich-output"))
        result.extend(_flag(args.yes, "--yes"))
        result.extend(_flag(args.skip_flutter_doctor, "--skip-flutter-doctor"))
        return result


class DoctorCommand(FletPassthroughCommand):
    """Show system and environment setup information."""

    command_name = "doctor"
    flet_subcommand = "doctor"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-v", "--verbose", action="count", default=0,
                            help="Enable verbose output")

    def _build_flet_args(self, args: Namespace) -> list[str]:
        return []
