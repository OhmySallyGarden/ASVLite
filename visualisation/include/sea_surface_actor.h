#ifndef SEA_SURFACE_ACTOR_H
#define SEA_SURFACE_ACTOR_H

#include "wave.h"
#include <vector>
#include <vtkSmartPointer.h>
#include <vtkPoints.h>
#include <vtkCellArray.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkPolyDataAlgorithm.h>
#include <vtkInformation.h>
#include <vtkInformationVector.h>

namespace asv_swarm
{
namespace Visualisation
{
/**
 * This class creates an actor for sea surface and provides visualization for 
 * class Hydrodynamics::Sea_surface_dynamics.
 */
class Sea_surface_actor : 
  public vtkPolyDataAlgorithm
{
public:
  /**
   * Constructor.
   */
  Sea_surface_actor(struct Wave* wave);

  /**
   * Increment time count.
   */
  void increment_time(){++timer_count;}

  /**
   * Set the step size for time increment.
   */
  void set_timer_step_size(unsigned int timer_step_size){
    this->timer_step_size = timer_step_size;
  }

  /**
   * Returns pointer to vtkActor object for sea surface.
   */
  vtkSmartPointer<vtkActor> get_actor(){return sea_surface_actor;}

protected:
  /**
   * This method is called by vtk pipeline and it sets the z values for the
   * control points in the mesh representing sea surface for the current time 
   * step.
   */
  virtual int RequestData(vtkInformation* request,
                          vtkInformationVector** inputVector,
                          vtkInformationVector* outputVector) override;

private:
  /** 
   * Method to set the compute the sea surface elevations at the grid points.
   * @param time in milliseconds from the start of simulation.
   */
  void set_sea_surface_elevations(unsigned long time);
  
private:
  unsigned long timer_count;
  unsigned int timer_step_size;
  vtkSmartPointer<vtkPoints> sea_surface_mesh_points {nullptr};
  vtkSmartPointer<vtkCellArray> sea_surface_mesh_cells {nullptr}; 
  vtkSmartPointer<vtkPolyDataMapper> sea_surface_mapper {nullptr};
  vtkSmartPointer<vtkActor> sea_surface_actor {nullptr};
  
  struct Wave* wave;
  std::vector<std::vector<Dimensions>> sea_surface_points;
  unsigned int sea_surface_grid_size;
}; // class Sea_surface_actor

} // namespace Visualisation
} // namespace asv_swarm

#endif // SEA_SURFACE_ACTOR_H
