import { Config } from "@remotion/cli/config";

// Rendu 100 % local : aucune donnée n'est envoyée à un service tiers.
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
