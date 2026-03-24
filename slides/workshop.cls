\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{integrity}[2025/11/14 Minimalistic Beamer Class for KIT/HMC Integrity]

% --- 1. CORE CLASS LOAD ---
% Load the standard beamer class. Using 16:9 aspect ratio.
\LoadClass[aspectratio=169]{beamer}

% --- 2. REQUIRED PACKAGES ---
\RequirePackage{fontspec} % Required for modern font handling (\setmainfont)
\RequirePackage{xcolor}   % Ensure colors are handled correctly

% --- 3. COLOR DEFINITIONS (KIT & HMC) ---
% Define the colors based on official branding
\definecolor{KITBlue}{RGB}{0, 98, 148}          % Karlsruhe Institute of Technology Primary
\definecolor{HMCBlue}{RGB}{0, 61, 76}           % Helmholtz Metadata Collaboration Primary
\definecolor{HMCAccent}{RGB}{242, 169, 0}       % HMC Accent Orange
\definecolor{LightGray}{RGB}{235, 235, 235}     % Used for block backgrounds

% --- 4. THEME APPLICATION (Explicit Minimal Look) ---
% Explicitly define the theme structure to ensure consistency and robust compilation
\usefonttheme{professionalfonts} % Ensures \setmainfont is respected
\useinnertheme{default}          % Simple title, item lists, and section page
\useoutertheme{miniframes}       % Minimalist header with section navigation dots

% --- 5. BEAMER COLOR SCHEMES (Minimal Setup) ---
% The color scheme drives the whole presentation's look.

% Primary Palette: Used for the header background
\setbeamercolor{palette primary}{fg=white,bg=KITBlue}
\setbeamercolor{section in head/foot}{fg=white, bg=KITBlue!70} % Section dots color

% Secondary Palette: Used for subsection navigation in the header
\setbeamercolor{palette secondary}{fg=white,bg=HMCBlue}

% Structure: Accent color for highlights, itemized lists, and link text
\setbeamercolor{structure}{fg=HMCAccent}
\setbeamercolor{title}{fg=HMCBlue} % Document Title color
\setbeamercolor{frametitle}{fg=HMCBlue, bg=white} % Frame Title color

% Blocks: Use KIT Blue for block titles and Light Gray for the block body
\setbeamercolor{block title}{fg=white, bg=KITBlue}
\setbeamercolor{block body}{fg=black, bg=LightGray}

% --- 6. FONT CONFIGURATION ---
% Use Noto Sans for a clean, professional look
\setmainfont{Noto Sans}

% --- 7. TEMPLATE CLEANUP ---
% Remove navigation symbols for a cleaner look.
\setbeamertemplate{navigation symbols}{} 

\endinput