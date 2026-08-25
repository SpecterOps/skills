set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# Show the available maintenance commands when invoked without a recipe.
default:
    @just --list

import 'tools/maintenance/just/core.just'
import 'tools/maintenance/just/go_review.just'
import 'tools/maintenance/just/activity_report.just'
import 'tools/maintenance/just/bloodhound.just'
import 'tools/maintenance/just/catalog.just'
import 'tools/maintenance/just/hygiene.just'
import 'tools/maintenance/just/portability.just'
import 'tools/maintenance/just/ci.just'
